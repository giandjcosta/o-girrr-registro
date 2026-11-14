#!/usr/bin/env python3
"""Server locale delle prove: supporta anche i Range di audio e video."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re


class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.range_bytes=None
        path=Path(self.translate_path(self.path))
        match=re.fullmatch(r'bytes=(\d*)-(\d*)',self.headers.get('Range',''))
        if not path.is_file() or not match or not any(match.groups()):
            return super().send_head()
        size=path.stat().st_size
        start=int(match[1]) if match[1] else max(0,size-int(match[2]))
        end=min(int(match[2]),size-1) if match[1] and match[2] else size-1
        if start>end or start>=size:
            self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
        file=path.open('rb');file.seek(start);self.range_bytes=end-start+1
        self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)))
        self.send_header('Content-Length',str(self.range_bytes));self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.send_header('Accept-Ranges','bytes');self.end_headers();return file

    def copyfile(self,source,output):
        if self.range_bytes is None:return super().copyfile(source,output)
        remaining=self.range_bytes
        while remaining:
            chunk=source.read(min(65536,remaining))
            if not chunk:break
            output.write(chunk);remaining-=len(chunk)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',default='.');p.add_argument('--port',type=int,default=8890)
    a=p.parse_args();ThreadingHTTPServer(('127.0.0.1',a.port),partial(RangeHandler,directory=a.directory)).serve_forever()
