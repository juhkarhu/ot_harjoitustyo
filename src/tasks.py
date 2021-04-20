from invoke import task


@task
def start(ctx):
    ctx.run('python main.py')


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")


@task
def test(ctx):
    ctx.run('pytest')


@task
def format(ctx):
    ctx.run('autopep8 --in-place --recursive ../src')


@task
def lint(ctx):
    ctx.run('pylint data')
