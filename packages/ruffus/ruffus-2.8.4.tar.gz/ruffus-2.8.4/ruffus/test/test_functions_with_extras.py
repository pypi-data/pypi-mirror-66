import glob
import uuid
import ruffus

N_FILES = 1000
N_EXTRAS = 10000


def create_file(outfile, extra):
    assert len(extra) == N_EXTRAS
    with open(outfile, "w") as outf:
        outf.write(outfile)


def transform_file(infile, outfile, extra):
    assert len(extra) == N_EXTRAS
    with open(outfile, "w") as outf:
        outf.write(outfile)


def transform_file_with_named_args(infile, outfile, extra):
    assert len(extra["background"]) == N_EXTRAS
    with open(outfile, "w") as outf:
        outf.write(outfile)


def originate_extras_with_string(tmp_path):

    pipeline = ruffus.Pipeline("originate_extras_with_string_{}".format(uuid.uuid4()))
    expected_files = ["{}/tmp_{}".format(tmp_path, x) for x in range(N_FILES)]
    pipeline.originate(
        task_func=create_file,
        output=expected_files,
        extras=["A" * N_EXTRAS])

    pipeline.run()
    return sorted(map(str, tmp_path.glob("*"))) == sorted(expected_files)


def originate_extras_with_list(tmp_path):

    pipeline = ruffus.Pipeline("originate_extras_with_list_{}".format(uuid.uuid4()))
    expected_files = ["{}/tmp_{}".format(tmp_path, x) for x in range(N_FILES)]
    pipeline.originate(
        task_func=create_file,
        output=expected_files,
        extras=[["file{}".format(x) for x in range(N_EXTRAS)]])

    pipeline.run()
    return sorted(map(str, tmp_path.glob("*"))) == sorted(expected_files)


def transform_extras_with_string(tmp_path):

    pipeline = ruffus.Pipeline("transform_extras_with_string_{}".format(uuid.uuid4()))
    input_files = ["{}/tmp_{}.in".format(tmp_path, x) for x in range(N_FILES)]
    for x in input_files:
        open(x, "w").close()

    expected_files = ["{}/tmp_{}.out".format(tmp_path, x) for x in range(N_FILES)]
    pipeline.transform(
        task_func=transform_file,
        input=input_files,
        output=".out",
        filter=ruffus.suffix(".in"),
        extras=["A" * N_EXTRAS])

    pipeline.run()
    return sorted(map(str, tmp_path.glob("*.out"))) == sorted(expected_files)


def transform_extras_with_list(tmp_path):

    pipeline = ruffus.Pipeline("transform_extras_with_list_{}".format(uuid.uuid4()))
    input_files = ["{}/tmp_{}.in".format(tmp_path, x) for x in range(N_FILES)]
    for x in input_files:
        open(x, "w").close()

    expected_files = ["{}/tmp_{}.out".format(tmp_path, x) for x in range(N_FILES)]
    pipeline.transform(
        task_func=transform_file,
        input=input_files,
        output=".out",
        filter=ruffus.suffix(".in"),
        extras=[["file{}".format(x) for x in range(N_EXTRAS)]])

    pipeline.run()
    return sorted(map(str, tmp_path.glob("*.out"))) == sorted(expected_files)


def transform_extras_with_container(tmp_path):

    pipeline = ruffus.Pipeline("transform_extras_with_container_{}".format(uuid.uuid4()))
    input_files = ["{}/tmp_{}.in".format(tmp_path, x) for x in range(N_FILES)]
    for x in input_files:
        open(x, "w").close()

    expected_files = ["{}/tmp_{}.out".format(tmp_path, x) for x in range(N_FILES)]
    pipeline.transform(
        task_func=transform_file_with_named_args,
        input=input_files,
        output=".out",
        filter=ruffus.suffix(".in"),
        extras=[{"background": ["file{}".format(x) for x in range(N_EXTRAS)]}])

    pipeline.run()
    return sorted(map(str, tmp_path.glob("*.out"))) == sorted(expected_files)


def test_originate_extras_with_string(benchmark, tmp_path):
    result = benchmark(originate_extras_with_string, tmp_path)
    assert result


def test_originate_extras_with_list(benchmark, tmp_path):
    result = benchmark(originate_extras_with_list, tmp_path)
    assert result


def test_transform_extras_with_string(benchmark, tmp_path):
    result = benchmark(transform_extras_with_string, tmp_path)
    assert result


def test_transform_extras_with_list(benchmark, tmp_path):
    result = benchmark(transform_extras_with_list, tmp_path)
    assert result


def test_transform_extras_with_container(benchmark, tmp_path):
    result = benchmark(transform_extras_with_container, tmp_path)
    assert result
