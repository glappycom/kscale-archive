<!-- preserved from https://docs.kscale.dev/os/klang via https://web.archive.org/web/20241214035356id_/https://docs.kscale.dev/os/klang -->

# Klang - K-Scale Docs

[Operating System](/os/intro "Operating System")Klang

# Klang

⚠️

This page is currently under construction.

```
cargo install klang  # To install the Klang toolchain
pip install pyklang  # To install the Python frontend
```

[Github](https://github.com/kscalelabs/klang)[Rust](https://crates.io/crates/klang)[Python](https://pypi.org/project/pyklang)

Klang is a domain-specific language (DSL) for programming robots.

![Klang Interface](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fklang-interface.ca82ee6d.png&w=3840&q=75)

Klang is built into K-Scale OS, and is designed to be a simple and flexible way to get started building robot applications. Right now, it is basically a glorified templating engine. Klang commands are executed by the neural interpreter described below. Here is a sample Klang program:

```
> wave [arm] arm {
    > wave joint [joint] twice {
        move joint [joint] on the [arm] arm to 90
        move joint [joint] on the [arm] arm to 0
    }

    " wave joint [1] twice
    " wave joint [2] twice
    " wave joint [3] twice
}

> wave both arms {
    " wave [right] arm
    " wave [left] arm
}

" wave both arms
```

The neural interpreter is responsible for executing these commands.

[End-to-End Model](/os/e2e "End-to-End Model")[Real-Time OS](/os/rtos "Real-Time OS")
