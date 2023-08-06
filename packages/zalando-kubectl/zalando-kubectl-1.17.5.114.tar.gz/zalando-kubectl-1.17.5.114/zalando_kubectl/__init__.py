# This is replaced during release process.
__version_suffix__ = '114'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.17.5"
KUBECTL_SHA512 = {
    "linux": "4cf67f972aad3425bccc48af83f8cb59ddcc96de49d3bb21cdbbcbbeee31718ef681e551d13343538a6e70c2a4ea0435e4540bc1f8cf1a91a2f73265f52b9429",
    "darwin": "fb7ff087cc82b930399c5512656de68a8b9c61f54e3bd3e627fff097e67a18411e0268b6cec0e40a96d596618002ccc2417deba5c0eba2dcb195813bdd40cc35",
}

STERN_VERSION = "1.11.0"
STERN_SHA256 = {
    "linux": "e0b39dc26f3a0c7596b2408e4fb8da533352b76aaffdc18c7ad28c833c9eb7db",
    "darwin": "7aea3b6691d47b3fb844dfc402905790665747c1e6c02c5cabdd41994533d7e9",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
