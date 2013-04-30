import sys
import json

charts = [
  {
    "name":"build",
    "data": (lambda x: x["results"]["build"]["time"]),
    "label": (lambda x: x["results"]["build"]["name"]),
    "title":"Initial Graph Construction",
    "y-axis":"Time (s)",
    "x-axis":"Graph Package",
  },
  {
    "name":"sv",
    "title":"Connected Components",
    "data": (lambda x: x["results"]["sv"]["time"]),
    "label": (lambda x: x["results"]["sv"]["name"]),
    "y-axis":"Time (s)",
    "x-axis":"Graph Package",
  },
  {
    "name":"pr",
    "title":"Page Rank",
    "data": (lambda x: x["results"]["pr"]["time"]),
    "label": (lambda x: x["results"]["pr"]["name"]),
    "y-axis":"Time (s)",
    "x-axis":"Graph Package",
  },
  {
    "name":"sssp",
    "title":"Single Source Shortest Path",
    "data": (lambda x: x["results"]["sssp"]["time"]),
    "label": (lambda x: x["results"]["sssp"]["name"]),
    "y-axis":"Time (s)",
    "x-axis":"Graph Package",
  },
  {
    "name":"update",
    "title":"Update Rate",
    "data": (lambda x: x["results"]["update"]["time"]),
    "label": (lambda x: x["results"]["update"]["name"]),
    "y-axis":"Edges per Second",
    "x-axis":"Graph Package",
  },
  {
    "name":"mem",
    "title":"Update Rate",
    "data": (lambda x: x["mem"]),
    "label": (lambda x: x["type"]),
    "y-axis":"Edges per Second",
    "x-axis":"Graph Package",
  },
]

def produce_bar_chart(chart, results, output):
  data = [chart["data"](r) for r in results]
  labels = [chart["label"](r) for r in results]
  output.write("""
<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>%s</title>

		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
		<script type="text/javascript">
		    $(function () {
			  $('#container').highcharts({
			      chart: {
				  type: 'column'
			      },
			      title: {
				  text: '%s'
			      },
			      xAxis: {
				  categories: %s
				  title: {
				      text: '%s'
				  }
			      },
			      yAxis: {
				  min: 0,
				  title: {
				      text: '%s'
				  }
			      },
			      series: [
				data: %s
			      ]
			  });
		      });
		</script>
	</head>
	<body>
<script src="js/highcharts.js"></script>
<script src="js/modules/exporting.js"></script>

<div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>

	</body>
</html>
  
  """ % (chart['title'], chart['title'], labels, chart['x-axis'], chart['y-axis'], data))

def parse_file(filename):
    fp = open(filename, 'r')
    text = fp.read()
    fp.close()

    decoder = json.JSONDecoder()
    end = text.find('{')
    sysconfig, end = decoder.raw_decode(text, idx=end)
    end += 1
    result, end = decoder.raw_decode(text, idx=end)
    return result, sysconfig
  

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Usage " + sys.argv[0] + " <prefix> resultsfile1 resultsfile2 ..."
    exit()

  results = []
  sysconfigs = []

  prefix = sys.argv[1]

  for a in sys.argv[2:]:
    result, sysconfig = parse_file(a)
    results.append(result)
    sysconfigs.append(sysconfig)

  for chart in charts:
    fp = open("charts/" + prefix + "." + chart["name"] + ".html", "w")
    produce_bar_chart(chart, results, fp)
    fp.close()
