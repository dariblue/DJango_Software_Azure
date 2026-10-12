from whitenoise.storage import CompressedManifestStaticFilesStorage

class LenientCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False
