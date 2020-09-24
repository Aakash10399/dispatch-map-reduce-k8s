# Dispatch-Map-Reduce Simple Implementation using Kubernetes
* Storage component contains persistent volume and claim manifest for storing input data
* Dispatcher component also handles Reducer responsibilities
* API for Dispatching and Task are decoupled into two separate components - API function upload_file and the class executeTask
* Map component - Wordcount - contains only the API implementation of the mapping task
* Sample input file - data.in
* Project documents