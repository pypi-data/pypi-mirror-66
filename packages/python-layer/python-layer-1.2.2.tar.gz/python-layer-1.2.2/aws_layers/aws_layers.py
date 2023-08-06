from pathlib import Path
import shutil
import subprocess
import datetime
from aws_layers.layer_utils import read_layer
from aws_layers.layer_utils import get_client
from aws_layers.layer_utils import get_layer_arn
from aws_layers.layer_utils import get_current_lambda_layers
import wget


def build_layer_zip(working_dir: str) -> str:
    """
    Build a zip file as layer
    inside current working directory
    :param working dir
    :return: a string with the file path
    """
    working_dir = Path(working_dir).absolute()
    output_dir_name = "python"

    output_dir_path = working_dir.joinpath(output_dir_name)
    Path.mkdir(output_dir_path)

    files = [
        e
        for e in working_dir.iterdir()
        if e.is_file() and e.name.split(".")[-1] == "py"
    ]

    requirements_file_path = working_dir.joinpath("requirements.txt")

    if files:
        for f in files:
            shutil.copy(str(f), output_dir_path.as_posix())
    status = subprocess.run(
        [
            "pip",
            "install",
            "-r",
            requirements_file_path.as_posix(),
            "-t",
            output_dir_path.as_posix(),
        ]
    ).returncode
    ts_now = int(datetime.datetime.timestamp(datetime.datetime.now()))

    if status == 0:
        shutil.make_archive(output_dir_path, "zip", working_dir, output_dir_name)
        shutil.rmtree(output_dir_path)
        zip_src_file_name = working_dir.joinpath(output_dir_name + ".zip").as_posix()
        zip_dest_file_name = working_dir.joinpath(
            working_dir.name + "_" + str(ts_now) + ".zip"
        )
        shutil.move(zip_src_file_name, zip_dest_file_name)

        return zip_dest_file_name

    return "Something went wrong"


def deploy_layer_zip(
    path_to_zip_file: str, description: str, runtime: str, aws_profile: str, region: str
) -> int:
    byte_stream = read_layer(path_to_zip_file, binary_file=True)
    layer_name = Path(path_to_zip_file).stem
    response = get_client(aws_profile, region).publish_layer_version(
        LayerName=layer_name,
        Description=description,
        Content={"ZipFile": byte_stream},
        CompatibleRuntimes=[runtime],
        LicenseInfo="string",
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]


def download_layer_zip(
    layer_name: str, version_number: int, aws_profile: str, region: str
) -> str:
    if not version_number:
        try:
            version_number = [
                l["Layer_version"]
                for l in list_all_layers()
                if l["Layer_name"] == layer_name
            ].pop()
        except IndexError:
            return "Empty version, wrong layer name?"

    try:
        response = get_client(aws_profile, region).get_layer_version(
            LayerName=layer_name, VersionNumber=version_number
        )
        download_url = response["Content"]["Location"]
        wget.download(download_url)
    except:
        return "The resource you requested does not exist."


def set_layer_to_lambda(
    layer_names: list,
    function_name: str,
    delete_old: bool,
    aws_profile: str = None,
    region: str = None,
) -> int:
    all_layers = list_all_layers(aws_profile, region)
    boto3_client = get_client(aws_profile, region)
    layers_arn = [
        get_layer_arn(layer_obj)
        for layer_obj in all_layers
        for layer_name in layer_names
        if layer_name == layer_obj["Layer_name"]
    ]

    if not delete_old:
        layers_arn.extend(get_current_lambda_layers(boto3_client, function_name))

    response = boto3_client.update_function_configuration(
        FunctionName=function_name, Layers=[*layers_arn]
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]


def list_all_layers(aws_profile: str = None, region: str = None) -> list:
    client = get_client(aws_profile, region)
    layers = client.list_layers()["Layers"]
    if layers:
        return [
            {
                "Layer_name": layer["LayerName"],
                "Layer_arn": layer["LayerArn"],
                "Layer_version": layer["LatestMatchingVersion"]["Version"],
            }
            for layer in layers
        ]
    return []
