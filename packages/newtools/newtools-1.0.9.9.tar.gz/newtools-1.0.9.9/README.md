# New Tools

Provides useful libraries for processing large data sets. 
Developed by the team at [www.dativa.com](https://www.dativa.com) as we find them useful in our projects.

The key libraries included here are:
* S3Location

#### S3Location
Class that parses out an S3 location from a passed string. Subclass of `str`
so supports most string operations.

Also contains properties .bucket, .key, .path, .prefix and method .join()

* param s3_str: string representation of s3 location, accepts most common formats
    ```
    eg:
        - 's3://bucket/folder/file.txt'
        - 'bucket/folder'
        - 'http[s]://s3*.amazonaws.com/bucket-name/'
    also accepts None if using `bucket` and `key` keyword
    ```
* param bucket: ignored if s3_str is not None. can specify only bucket for
    bucket='mybucket' - 's3://mybucket/' or in conjuction with `key`
* param key: ignored if s3_str is not None. Bucket must be set.
    bucket='mybucket', key='path/to/file' - 's3://mybucket/path/to/file'
* param ignore_double_slash: default False. If true allows s3 locations containing '//'
    these are valid s3 paths, but typically result from mistaken joins


