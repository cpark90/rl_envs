package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("@python_deps//:requirements.bzl", "requirement")


filegroup(
    name = "random_walk_src",
    srcs = glob(["random_walk/**/*.py"])
)

py_library(
    name = "random_walk",
    srcs = [
        ":random_walk_src",
    ],
    deps = [
        requirement("gymnasium"),
        requirement("numpy"),
    ],
)

py_library(
    name = "envs",
    srcs = [
        "__init__.py",
    ],
    deps = [
        requirement("gymnasium"),
        ":random_walk",
    ],
)