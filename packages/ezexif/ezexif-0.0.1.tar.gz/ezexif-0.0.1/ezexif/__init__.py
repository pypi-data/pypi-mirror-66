import exifread
from collections import defaultdict

def process_file(filename, stop_tag='UNDEF', details=True, strict=False, debug=False, truncate_tags=True, auto_seek=True, raw=False):
    """
    Wrapper for origin exifread.process_file.
    Process an image file (expects a image filename).
    This is the function that has to deal with all the arbitrary nasty bits
    of the EXIF standard.
    """

    with open(filename, "rb") as f:
        tags = exifread.process_file(f, stop_tag, details, strict, debug)

        # return the raw tags dict when it is empty or raw is set to True
        if not tags or raw:
            return tags

        # easy and safe to read
        ezTags = defaultdict(lambda:defaultdict(str))

        # get all tag printable values and divide categories to dicts
        for key, tagObj in tags.items():
            keyNames = key.split()
            tagName = keyNames[0]
            ifdName = keyNames[1] if len(keyNames) > 1 else ""

            if not ifdName:
                ezTags[tagName] = tagObj.printable if tagObj else tagObj
            else:
                ezTags[tagName][ifdName] = tagObj.printable if tagObj else tagObj
        
        return ezTags