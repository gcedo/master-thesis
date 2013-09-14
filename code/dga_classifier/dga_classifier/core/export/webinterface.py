########################################
## Web interface generator
########################################

class WebInterfaceGenerator:
	def __init__(self):
		pass

	def generate(self, file_name, js):
		HTML_page = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Timeline viewer</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript">
    google.load('visualization', '1', {packages: ['annotatedtimeline']});""" + js + """
    google.setOnLoadCallback(drawVisualization);
  </script>
</head>
<body style="font-family: Arial;border: 0 none;">
</br></br></br>
<span id="title"></span>
</br></br>
<div id="visualization" style="width: 100%; height: 600px; margin-left: auto; margin-right: auto;"></div>
</body>
</html>"""

		FILE = open(file_name, "w")
		FILE.write(HTML_page)
		FILE.close()