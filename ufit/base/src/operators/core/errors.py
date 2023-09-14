import os
import time
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import webbrowser
from .wetransfertool import We
from ..utils.sorting import natural_sort
from ..utils.user_interface import get_addon_version


def create_report_zip(context):
    checkpoints = os.listdir(context.scene.ufit_folder_checkpoints)

    report_files = []

    if checkpoints:
        # add the scan file to the report_files
        for file in os.listdir(context.scene.ufit_folder_modeling):
            if file.endswith('.zip'):
                report_files.append(f'{context.scene.ufit_folder_modeling}/{file}')

        # get and sort the blend files
        blend_files = [c for c in checkpoints if (c.startswith('ST_') and c.endswith('.blend'))]
        blend_files_sorted = natural_sort(blend_files)

        # get the last two blender files
        report_blend_files = [f'{context.scene.ufit_folder_checkpoints}/{f}' for f in blend_files_sorted[-2:]]

        # add the last two blender files to the report_files
        report_files.extend(report_blend_files)

        # create zip file with report_files
        modeling_dir = pathlib.Path(context.scene.ufit_folder_modeling)
        report_zip = f'{modeling_dir}_error.zip'
        with ZipFile(report_zip, mode="w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for filename in report_files:
                archive.write(filename,
                              arcname=os.path.basename(filename))

        return report_zip

    return None


def wetransfer_upload(path):
    wt = We()
    wt_metadata = wt.upload(path,
                            display_name='uFit - Blender Error')

    return wt_metadata.get('shortened_url')


def open_email_client(recipient, subject, body):
    webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)


def report_problem(context):
    report_zip_file = create_report_zip(context)

    # try 10 times to make the wetransfer link
    wetransfer_link = None
    for i in range(10):
        try:
            wetransfer_link = wetransfer_upload(report_zip_file)
            break
        except Exception as e:
            print(e)
            pass
        time.sleep(2)

    recipient = 'ufit@ugani.org'
    subject = 'uFit - Report Problem'
    ufit_version = get_addon_version('uFit')
    if wetransfer_link:
        body = f'uFit checkpoint files are uploaded to {wetransfer_link} and are ready for further investigation. %0D%0A %0D%0A' \
               f'Problem encountered by uFit user: {context.scene.ufit_user} %0D%0A %0D%0A' \
               f'uFit version: {ufit_version} %0D%0A %0D%0A' \
               f'Problem description:%0D%0A' \
               f'[Please provide a short problem description here and then send the email]'
    else:
        body = f'The system did not succeed in uploading the files to WeTransfer. ' \
               f'Please manually attach the last two checkpoint files (.blend) and the 3D scan for the uFit team.' \
               f'Problem encountered by uFit user: {context.scene.ufit_user} %0D%0A %0D%0A' \
               f'uFit version: {ufit_version} %0D%0A %0D%0A' \
               f'Problem description:%0D%0A' \
               f'[Please provide a short problem description here and then send the email]'

    open_email_client(recipient=recipient,
                      subject=subject,
                      body=body)
