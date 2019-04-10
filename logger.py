from covicas.db_plugin import Database
from covicas.settings import settings
from absl import app, flags
FLAGS = flags.FLAGS
flags.DEFINE_string("settings","abcd.json","Settings File tp Load From")
flags.DEFINE_boolean("follow", False, "Follow the Log")
def main(_):
  s = settings(FLAGS.settings)
  d = Database()
  d.display(follow = FLAGS.follow)
if __name__ == "__main__":
  app.run(main)

