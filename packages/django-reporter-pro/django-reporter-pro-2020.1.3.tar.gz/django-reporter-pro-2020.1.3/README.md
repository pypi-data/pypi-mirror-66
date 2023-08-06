# Django Reporter Pro

### Setup in your django project:

* Clone into `django_reporter` folder of you `project's root` directory
	```bash
	 git clone git@github.com:shamilison/django-reporter-pro.git <reporting_cloned_folder_name>
	```
* Add reporter.pth file in your python environment's site-package folder where content will be
	```bash
	import sys;sys.__plen = len(sys.path)
	/{path_to_<reporting_cloned_folder_name>}/
	import sys; new=sys.path[sys.__plen:];del sys.path[sys.__plen:];p=getattr(sys,'__egginsert',0);sys.path[p:p]=new;sys.__egginsert = p+len(new);
	```
* Add in settings settings.py
	```python
	WEBPACK_APPLICATION_STATS_PATH = os.path.join(os.path.join(BASE_DIR, '<reporting_cloned_folder_name>'), 
													'django_report_vue', 'webpack-application-stats.json')
	# WEBPACK_APPLICATION_STATS_PATH has to be path to the file of "<reporting_cloned_folder_name>/django_report_vue/webpack-application-stats.json"
	WEBPACK_LOADER = {
	    'DJANGO_REPORT_PRO': {
	        'CACHE': not DEBUG,
	        'BUNDLE_DIR_NAME': '/bundles/',  # must end with slash
	        'STATS_FILE': WEBPACK_APPLICATION_STATS_PATH,
	    },
	}
	```
* Add apps in our installed app's list
	```bash
	# Vuejs Integration Helpers
    'webpack_loader',
    'corsheaders',
   
	# Reporter app
	'django_reporter_pro',
	```
* Include urls of reporter library in your project urls.py
url(r'^', include('django_reporter_pro.urls')),
* These are the URLS:
	```bash
	/django-reporter/#/build-report/create/ - to create report
	/django-reporter/#/build-report/update/{pk}/ - to update report
	/django-reporter/#/build-report/view/{pk}/ - to view the report output
	```
* Install required python packages as follows:
	```bash
	cd <reporting_cloned_folder_name>
	pip install -r packages.txt
	```
* Run `python manage.py migrate` to introduce `django_reporter_pro` module models
* Here `<reporting_cloned_folder_name>/django_report_vue` is a standalone VueJS project:
	Go to `<reporting_cloned_folder_name>/django_report_vue` and run:
	```bash
	npm install
	npm run serve
	```
	This will update a `webpack-application-stats.json` file for your django project's webpack.
* Use following decorator over a model to make it available for reporter: `enable_for_reporter`