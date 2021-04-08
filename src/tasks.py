from invoke import task


@task
def start(ctx):
	ctx.run('python main.py')
