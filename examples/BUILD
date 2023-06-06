package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_binary")
load("@python_deps//:requirements.bzl", "requirement")


py_binary(
    name = "random_walk_example",
    srcs = [
        "random_walk_example.py",
    ],
    deps = [
        requirement("gymnasium"),
        requirement("numpy"),
        requirement("six"),
        "//envs",
    ],
)