# changelog
### v0.5
* Added support for deletesandbox.do
* Changed Dockerfile to utilize a Python distro that is better supported by the Demo Labs
--------
### v0.4
--------
* RENUMBERED VERSIONS to match the [Semantic Versioning 2.0.0 standard](https://semver.org/)
** Previous version names were v1.0-v1.2
* Added in a "Credentials Check" before actually running through the CSV file, which causes the script to exit on an error.
** This check makes sure that the specified credentials can be used to successfully call getmaintenancescheduleinfo.do
* Improved overall error-trapping throughout bulkupload.py and new_api.py
--------
### v0.3
* Utilizes Dockerfile and requirements.txt to get all dependencies
--------
### v0.2
* Removed debug and commented code
* Refactored logging functionality into its own class to be utilized by multiple modules
* Log file created is based upon filename used
--------
### v0.1
* Initial code push