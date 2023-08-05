from slurmpie import slurmpie
import pytest


def test_init():
    slurmpie.Pipeline()

    pipeline = slurmpie.Pipeline(name="test_pipeline")
    assert pipeline.job_args == {"name": "test_pipeline"}


def test_job_adding():
    pipeline = slurmpie.Pipeline()

    job = slurmpie.Job("none")
    pipeline.add(job)
    second_job = slurmpie.Job("none")
    pipeline.add(second_job)

    assert isinstance(pipeline.pipeline_jobs, list)
    assert len(pipeline.pipeline_jobs) == 2
    assert pipeline._job_graph == {-1: [job], second_job: {"afterany": [job._id]}}


def test_job_adding_with_job_arguments():
    job = slurmpie.Job("none")
    pipeline = slurmpie.Pipeline(name="test_pipeline", memory_size="10GB")

    pipeline.add(job)
    pipeline.add(job)

    for job in pipeline.pipeline_jobs:
        assert job.name == "test_pipeline"
        assert job.memory_size == "10G"

    job_with_args = slurmpie.Job("none", name="final_job", memory_size="15MB")
    pipeline.add(job_with_args)

    for job in pipeline.pipeline_jobs[:-1]:
        assert job.name == "test_pipeline"
        assert job.memory_size == "10G"

    assert pipeline.pipeline_jobs[-1].name == "final_job"
    assert pipeline.pipeline_jobs[-1].memory_size == "15M"


def test_start_job_adding():
    job = slurmpie.Job("none")
    pipeline = slurmpie.Pipeline()

    pipeline.add(job)

    success_job = slurmpie.Job("none")
    pipeline.add(success_job)

    second_start_job = slurmpie.Job("none")
    pipeline.add_start_job(second_start_job)

    assert pipeline._job_graph == {
        -1: [job, second_start_job],
        success_job: {"afterany": [job._id]},
    }


def test_complex_job_adding():
    job = slurmpie.Job("none")
    pipeline = slurmpie.Pipeline()

    pipeline.add(job)
    assert pipeline._job_graph == {-1: [job]}

    second_job = slurmpie.Job("none")
    pipeline.add({"afterok": [second_job]})

    assert isinstance(pipeline.pipeline_jobs, list)
    assert len(pipeline.pipeline_jobs) == 2

    assert pipeline._job_graph == {-1: [job], second_job: {"afterok": [job._id]}}

    fail_job = slurmpie.Job("none")
    pipeline.add({"afternotok": [fail_job]}, job)

    assert pipeline._job_graph == {
        -1: [job],
        second_job: {"afterok": [job._id]},
        fail_job: {"afternotok": [job._id]}
    }

    second_succes_job = slurmpie.Job("none")
    pipeline.add({"afterok": [second_succes_job]}, job)
    assert pipeline._job_graph == {
        -1: [job],
        second_job: {"afterok": [job._id]},
        fail_job: {"afternotok": [job._id]},
        second_succes_job: {"afterok": [job._id]}
    }

    final_job = slurmpie.Job("none")
    pipeline.add(final_job)

    assert pipeline._job_graph == {
        -1: [job],
        second_job: {"afterok": [job._id]},
        fail_job: {"afternotok": [job._id]},
        second_succes_job: {"afterok": [job._id]},
        final_job: {"afterany": [second_succes_job._id]}
    }

    pipeline.add(fail_job, second_job)

    assert pipeline._job_graph == {
        -1: [job],
        second_job: {"afterok": [job._id]},
        fail_job: {"afternotok": [job._id], "afterany": [second_job._id]},
        second_succes_job: {"afterok": [job._id]},
        final_job: {"afterany": [second_succes_job._id]}
    }

    pipeline.add(fail_job, second_succes_job)
    assert pipeline._job_graph == {
        -1: [job],
        second_job: {"afterok": [job._id]},
        fail_job: {"afternotok": [job._id], "afterany": [second_job._id, second_succes_job._id]},
        second_succes_job: {"afterok": [job._id]},
        final_job: {"afterany": [second_succes_job._id]}
    }

# These tests only work when slurm is installed

# def test_submit():
#     pipeline = slurmpie.Pipeline()

#     job = slurmpie.Job("none")
#     pipeline.add(job)
#     second_job = slurmpie.Job("none")
#     pipeline.add(second_job)

#     pipeline.submit()


# def test_submit_error():
#     with pytest.raises(RecursionError):
#         pipeline = slurmpie.Pipeline()

#         job = slurmpie.Job("none")
#         pipeline.add(job)
#         second_job = slurmpie.Job("none")
#         third_job = slurmpie.Job("none")
#         pipeline.add(second_job, third_job)
#         pipeline.add(third_job, second_job)

#         pipeline.submit()
