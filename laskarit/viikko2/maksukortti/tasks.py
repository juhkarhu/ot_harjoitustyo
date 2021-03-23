from invoke import task

@task
def test(ctx):
    ctx.run('pytest')


@task
def coverage(ctx):
    ctx.run('coverage run --branch -m pytest')

@task(coverage)
def coverage_report(ctx):
    # ctx.run('coverage report -m')
    ctx.run('coverage html')