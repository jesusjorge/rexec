import builtins
from datetime import datetime
import io
import os
import requests
import types
import urllib3
from urllib.parse import urlparse
import uuid
import warnings
import xml.etree.ElementTree as ET

class U:
    @classmethod
    @property
    def basePath(cls):
        return "C:\\ProgramData\\lib"

    @classmethod
    @property
    def pathSep(cls):
        return os.path.sep

    @classmethod
    @property
    def timestamp(cls):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    @classmethod
    @property
    def uuid(cls):
        return str(uuid.uuid4())

    @classmethod
    def pathConcat(cls,*path):
        if len(path) == 1:
            return path[0]
        result = [path[0]]
        for segment in path[1:]:
            result.append(U.pathSep)
            result.append(segment)
        return "".join(result)

    @classmethod
    def dir(cls,path):
        return os.listdir(path)

    @classmethod
    def delFile(cls,path):
        if os.path.isfile(path):
            os.remove(path)
        
    @classmethod
    def read(cls, url,ignoreError=False):
        uri = urlparse(url)
        result = None
        if uri.scheme in ["http","https"]:
            if ignoreError:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            result = requests.get(url,verify=(not ignoreError)).content
            if ignoreError:
                warnings.resetwarnings()
        else:
            try:
                with builtins.open(url, 'rb') as file:
                    result = file.read()
            except Exception as e:
                if ignoreError == False:
                    raise e
                else:
                    result = None
        return result

    @classmethod
    def write(cls,path,content):
        if type(content) is str:
            content = content.encode('utf-8')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            file.write(content)

    @classmethod
    def rexec(cls,url,*params):
        namespace = {"U":U}
        script = cls.Cache.read(url).decode('utf-8')
        exec(script,namespace)
        returns = namespace.get("returns")
        if type(returns) is types.FunctionType:
            return returns(*params)
#################################################################################################################################
    class Cache:
        @classmethod
        @property
        def _indexDoc(cls):
            content = U.read(U.pathConcat(U.basePath,"Cache","index.xml"),ignoreError=True) or b'<index></index>'
            return ET.fromstring(content.decode("utf-8"))

        @classmethod
        def _setIndexDoc(cls,doc):
            tree = ET.ElementTree(doc)
            with io.BytesIO() as xml_bytes_io:
                tree.write(xml_bytes_io, encoding='utf-8', xml_declaration=True)
                U.write(U.pathConcat(U.basePath,"Cache","index.xml"),xml_bytes_io.getvalue())

        @classmethod
        def Url2UUID(cls,url):
            doc = cls._indexDoc
            entry = doc.find(f".//entry[@url='{url}']")
            if entry is None:
                uuid = U.uuid
                entry = ET.Element("entry")
                entry.set("uuid",uuid)
                entry.set("url",url)
                doc.append(entry)
                cls._setIndexDoc(doc)
                return uuid
            else:
                return entry.get("uuid")

        @classmethod
        def remove(cls,url):
            uri = urlparse(url)
            if uri.scheme in ["http","https"]:
                uuid = cls.Url2UUID(url)
                path = U.pathConcat(U.basePath,"Cache","Content",uuid)
                U.delFile(path)

        @classmethod
        def read(cls,url,minLen=0):
            uri = urlparse(url)
            if uri.scheme in ["http","https"]:
                uuid = cls.Url2UUID(url)
                path = U.pathConcat(U.basePath,"Cache","Content",uuid)
                content = U.read(path,ignoreError=True)
                if content is None or len(content) < minLen:
                    content = U.read(url,ignoreError=True)
                    if len(content) > minLen:
                        U.write(path,content)
                return content
            else:
                return U.read(url)
    
    @classmethod
    @property
    def help(cls):
        return f"""
----------------------------------------------------------------------
class U:

<Properties>
    U.basePath -> {U.basePath}
        returns the configured base path

    U.pathSep -> {U.pathSep}
        returns the path separator character

    U.timestamp -> {U.timestamp}
        returns the current timestamp in YYYYMMDDhhmmss format

    U.uuid -> {U.uuid}
        returns a new UUID
        
<Methods>
    U.pathConcat(U.basePath,dir1,filename) -> {U.pathConcat(U.basePath,'dir1','filename')}
        concatenates a path using the current platform separator

    U.dir(U.basePath) -> {str(U.dir(U.basePath))}
        retrieves the content of a folder, files and folders

    U.delFile(filepath) ->
        deletes a file, if it exists

    U.read(url,ignoreError=True) -> b"Contents of a file or webpage in binary"
        retrieves content from http, https, or local filesystem

    U.write(U.pathConcat(U.basePath,"A","B","C.txt"),"Hi!") -> {U.write(U.pathConcat(U.basePath,"A","B","C.txt"),"Hi --!")}
        writes a file

    U.rexec(url,*params) -> returns(*params) ->
        using Cache.read(), downloads and stores the url, executes the code, and if it finds def returns(*params):, it executes it and gets the result

<Classes>
    Cache
        Handles everything related U.read(), but stores the result
----------------------------------------------------------------------
"""
