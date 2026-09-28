<!-- preserved from https://docs.kscale.dev/pkg/intro via https://web.archive.org/web/20241214031336id_/https://docs.kscale.dev/pkg/intro -->

# K-Scale API - K-Scale Docs

PlatformIntroduction

# K-Scale API

The K-Scale API is a way to programmatically interact with the K-Scale platform. It is available in Python, Rust, and as a CLI.

## Installation

First, you need to get an API key from [here](https://kscale.dev/keys), then export it as an environment variable:

```
export KSCALE_API_KEY='your-api-key'
```

### Python

To install the Python API, use `pip`:

```
pip install kscale
```

This will also install the `kscale` CLI.

### Rust

To install just the Rust component of the API, use `cargo`:

```
cargo add kscale
```

[Code Signing](/os/signing "Code Signing")[Command Line Interface](/pkg/cli "Command Line Interface")
