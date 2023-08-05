from matplotlib import pyplot as plt
from app.database import update_store_reports
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import click
import time
import os

cong_report = {
	"pan": {
		"total_records": {
			"total": 0,
			"correct": 0,
			"incorrect": 0
		},
		"date": {
			"correct": 0,
			"incorrect": 0
		},
		"month": {
			"correct": 0,
			"incorrect": 0
		},
		"year": {
			"correct": 0,
			"incorrect": 0
		},
		"pan_id": {
			"correct": 0,
			"incorrect": 0
		},
		"name": {
			"correct": 0,
			"incorrect": 0
		},
		"father_name": {
			"correct": 0,
			"incorrect": 0
		}

	}
}


def match_records(document, file_name, hcd_records, ocrd_records):

	record_flag = 0
	if document == "pan":

		try:
			for index, record in enumerate(hcd_records):
				ocrd = ocrd_records[index]
				hcd = hcd_records[index]

				# if index != 0:
				#     print(cong_report['pan'])
				#     import time
				#     time.sleep(2)
				# print(ocrd)
				# print(hcd)
				# print('\n')

				cong_report['pan']['total_records']['total'] += 1
				try:
					if ocrd != None:
						if hcd['name'] == ocrd['name']:
							cong_report['pan']['name']['correct'] += 1
						else:
							cong_report['pan']['name']['incorrect'] += 1
							record_flag = 1
						if hcd['father_name'] == ocrd['father_name']:
							cong_report['pan']['father_name']['correct'] += 1
						else:
							cong_report['pan']['father_name']['incorrect'] += 1
							record_flag = 1

						if 'pan_id' in ocrd.keys() and hcd['pan_id'] == ocrd['pan_id']:
							cong_report['pan']['pan_id']['correct'] += 1
						else:
							cong_report['pan']['pan_id']['incorrect'] += 1
							record_flag = 1
						if 'date' in ocrd.keys():
							if hcd['date'] == ocrd['date']:
								cong_report['pan']['date']['correct'] += 1
						else:
							cong_report['pan']['date']['incorrect'] += 1
							record_flag = 1
						if 'month' in ocrd.keys():
							if hcd['month'] == ocrd['month']:
								cong_report['pan']['month']['correct'] += 1
						else:
							cong_report['pan']['month']['incorrect'] += 1
							record_flag = 1
						if 'year' in ocrd.keys():
							if hcd['year'] == ocrd['year']:
								cong_report['pan']['year']['correct'] += 1
						else:
							cong_report['pan']['year']['incorrect'] += 1
							record_flag = 1
					else:
						record_flag = 1

					if record_flag == 0:
						cong_report['pan']['total_records']['correct'] += 1
					else:
						cong_report['pan']['total_records']['incorrect'] += 1
				except Exception as e:
					click.secho('congruous : ' + str(e), fg="red")

			cong_report['pan']['report_id'] = str(int(time.time()))
			click.echo("congruous : match report id  	: #" +
					   cong_report['pan']['report_id'])
			click.echo("congruous : match report file  	: " + file_name)
			click.echo("congruous : total records    	: " +
					   str(cong_report['pan']['total_records']['total']))
			click.echo("congruous : matched records  	: " +
					   str(cong_report['pan']['total_records']['correct']))
			click.echo("congruous : mismatched records  : " +
					   str(cong_report['pan']['total_records']['incorrect']))
			accuracy = round((cong_report['pan']['total_records']['correct'] /
							  cong_report['pan']['total_records']['total']) * 100)
			cong_report['pan']['accuracy'] = accuracy
			click.echo("congruous : accuracy percentage : " +
					   str(accuracy) + "%")
			update_store_reports(document, file_name, cong_report)

			# generate_match_report(document)

			test_function_call()

		except Exception as e:
			click.secho('congruous : ' + str(e), fg="red")
		return

def test_function_call():
	for field in cong_report['pan'].keys():
		if field == "total_records" : 
			pass
		else:
			print("congruous : " + str(field) + " match	 	: " + str(cong_report['pan'][field]["correct"]))
			print("congruous : " + str(field) + " mismatch 	: " + str(cong_report['pan'][field]["incorrect"]))


def generate_match_report(document):

	file_name=cong_report[document]['report_id'] + ".pdf"
	chart_image=show_pie_charts(document)

	title="Congruous Match Report"
	pdf=canvas.Canvas(file_name)
	pdf.setTitle(title)
	# drawMyRuler(pdf)

	# Set Logo
	image='app/assets/logo.png'
	pdf.drawInlineImage(image, 40, 720)

	# Register font
	pdfmetrics.registerFont(
		TTFont('abc', 'app/assets/OpenSans-Bold.ttf')
	)

	# Center the title and write
	pdf.setFont("abc", 24)
	pdf.drawCentredString(320, 750, title)

	# Draw a line below the title
	pdf.line(50, 730, 500, 730)

	# Set the date
	report_date="Date: " + datetime.now().strftime("%d/%m/%Y")
	pdfmetrics.registerFont(
		TTFont('abc', 'app/assets//OpenSans-Regular.ttf')
	)
	pdf.setFont("abc", 12)
	report=pdf.beginText(450, 680)
	report.textOut(report_date)
	pdf.drawText(report)

	# Set the report Id
	report_id="Report no.: #8058900"
	pdfmetrics.registerFont(
		TTFont('abc', 'app/assets/OpenSans-Regular.ttf')
	)

	pdf.setFont('abc', 12)
	report=pdf.beginText(50, 680)
	report.textOut(report_id)
	pdf.drawText(report)

	report_description="The following pie-charts depicts the match percentage of custom-built OCR parsed data with its human curated data."
	pdfmetrics.registerFont(
		TTFont('abc', 'app/assets/OpenSans-Light.ttf')
	)

	pdf.setFont('abc', 9)
	report=pdf.beginText(50, 630)
	report.textOut(report_description)
	pdf.drawText(report)

	# Set piechart
	# pdf.drawInlineImage(chart_image, 100, 0)
	# os.remove(chart_image)

	pdf.save()


def show_pie_charts(document):

	print(cong_report)

	if document == 'pan':
		fig=plt.figure()

		slices_total=[cong_report[document]['total_records']['correct'],
						cong_report[document]['total_records']['incorrect']]
		color_total=['#47B39C', '#EC6B56']

		slices_pan=[cong_report[document]['pan_id']['correct'],
					  cong_report[document]['pan_id']['incorrect']]
		color_pan=['#47B39C', '#EC6B56']

		slices_date=[cong_report[document]['date']['correct'],
					   cong_report[document]['date']['incorrect']]
		color_date=['#47B39C', '#EC6B56']

		slices_month=[cong_report[document]['month']['correct'],
						cong_report[document]['month']['incorrect']]
		color_month=['#47B39C', '#EC6B56']

		slices_year=[cong_report[document]['year']['correct'],
					   cong_report[document]['year']['incorrect']]
		color_year=['#47B39C', '#EC6B56']

		slices_name=[cong_report[document]['name']['correct'],
					  cong_report[document]['name']['incorrect']]
		color_name=['#47B39C', '#EC6B56']

		slices_father_name=[cong_report[document]['father_name']['correct'],
							 cong_report[document]['father_name']['incorrect']]
		color_name=['#47B39C', '#EC6B56']

		ax1=fig.add_axes([0, 0, .4, .4], aspect=1)
		ax1.pie(slices_total, labels=slices_total, colors=color_total,
				wedgeprops={'edgecolor': 'black'}, autopct='%1.0f%%', radius=1.7)

		ax2=fig.add_axes([1, 0, .4, .4], aspect=1)
		ax2.pie(slices_pan, labels=slices_pan, colors=color_pan, wedgeprops={
				'edgecolor': 'black'}, autopct='%1.0f%%', radius=1.7)

		ax3=fig.add_axes([0, 1, .4, .4], aspect=1)
		ax3.pie(slices_date, labels=slices_date, colors=color_date, wedgeprops={
				'edgecolor': 'black'}, autopct='%1.0f%%', radius=1.7)

		ax4=fig.add_axes([1, 1, .4, .4], aspect=1)
		ax4.pie(slices_month, labels=slices_month, colors=color_date,
				wedgeprops={'edgecolor': 'black'}, autopct='%1.0f%%', radius=1.7)

		ax5=fig.add_axes([0, 2, .4, .4], aspect=1)
		ax5.pie(slices_year, labels=slices_year, colors=color_date, wedgeprops={
				'edgecolor': 'black'}, autopct='%1.0f%%', radius=1.7)

		ax6=fig.add_axes([1, 2, .4, .4], aspect=1)
		ax6.pie(slices_year, labels=slices_name, colors=color_name, wedgeprops={
			'edgecolor': 'black'}, autopct='%1.0f%%', radius=1.7)

		ax1.set_title('Complete Record Match %\n\n\n\n')
		ax2.set_title('Pan Number Match %\n\n\n')
		ax3.set_title('DOB Date Match %\n\n\n')
		ax4.set_title('DOB Month Match %\n\n\n')
		ax5.set_title('DOB Year Match %\n\n\n')
		ax6.set_title('Name Match %\n\n\n')

		# import os
		# print(os.getcwd())
		my_dpi=96
		plt.figure(figsize=(500 / my_dpi, 700 / my_dpi), dpi=my_dpi)
		plt.savefig(cong_report[document]['report_id'] + \
		            '.png',  bbox_inches='tight')
		# plt.show()

		return cong_report[document]['report_id'] + '.png'
