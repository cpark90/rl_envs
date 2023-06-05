#WORKSPACE
workspace(name = "rl_envs")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

load("//bazel-scripts:rl_envs_rules.bzl", "rl_envs_rules")
rl_envs_rules()


# python
load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

load("@rules_python//python:pip.bzl", "pip_parse")
pip_parse(
    name = "python_deps",
    requirements_lock = "//third_party:requirements.txt",
)

load("@python_deps//:requirements.bzl", "install_deps")
install_deps()


# Docker
# Download the rules_docker repository at release v0.14.4
load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
container_repositories()

load(
    "@io_bazel_rules_docker//python:image.bzl",
    _py_image_repos = "repositories",
)
_py_image_repos()


# protocol buffer

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies")

rules_proto_dependencies()

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()


# maven

load("//bazel-scripts:rl_envs_java_deps.bzl", "rl_envs_java_deps")
rl_envs_java_deps()