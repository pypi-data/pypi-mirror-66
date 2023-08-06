import requests
import six
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor


class ProgressBar(tqdm):

    def update_to(self, n):
        """
        identical to update, except `n` should be current value and not delta.
        """
        self.update(n - self.n)


def upload(destination, file, progress_bar=False):
    url = destination['url']
    fields = destination['fields']
    fields['file'] = (
        'features_backup.rcdb', file
    )
    encoder = MultipartEncoder(fields=fields)
    if not progress_bar:
        return requests.post(url, data=encoder, headers={
            'Content-Type': encoder.content_type
        })

    with ProgressBar(total=encoder.len, unit='bytes', unit_scale=True, leave=False) as bar:
        monitor = MultipartEncoderMonitor(encoder, lambda monitor: bar.update_to(monitor.bytes_read))
        return requests.post(url, data=monitor, headers={
            'Content-Type': encoder.content_type
        })


def download(source, destination=None):
    is_file = False
    if destination is None:
        fp = six.BytesIO()
    elif isinstance(destination, six.BytesIO) or isinstance(destination, six.StringIO):
        fp = destination
    else:
        fp = open(destination, 'wb')
        is_file = True

    r = requests.get(source, stream=True)
    file_size = int(r.headers['Content-Length'])
    chunk, chunk_size = 1, 1024
    with ProgressBar(total=file_size, unit='bytes', unit_scale=True, leave=False) as bar:
        for chunk in ProgressBar(
            r.iter_content(chunk_size)
        ):
            fp.write(chunk)

    if is_file:
        fp.close()
        return destination
    return fp
