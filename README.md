# groot

groot - documentation

groot is a library that is designed for data scientists. The library’s purpose is to wrap all the machine learning pipeline, deploy it and monitor it. It will achieve this goal by wrapping each section of the pipeline, connecting them together after and using different methods in order to deploy it.

Task
This class is a class that defines a wrapped section of machine learning. This class is abstract, so in order to create a task, you will need to inherit from this class.

The class contains a few properties:
task_id - The id of the task.
max_retries -  How many retries the task will have.
name - The name of the task.
exceptions_retry - A dictionary that contains exceptions and a boolean value which determines if the user wants to check this exception in its code or not.
is_task_failed -  a boolean variable that states if the task has failed or not.
The constructor contains the following parameters: task_id, max_retries, name, exceptions_retry

In addition, the class contains two other functions:
action(user_input: Any | None)
The function’s purpose is to wrap the user’s code. It receives one input from the user and returns according to the user’s code.
The input of the function could be of any type.

on_failure()
The function’s purpose is to define what will happen if the action() function fails and the exceptions that returned from the action() function are in the exceptions_retry dict.




Moreover, I have created some built-in tasks for you.

DefaultModelTask
This task’s purpose is to implement your model and to allow accessibility to it.
The model you implement should be saved in a pickle file, and contains a 'predict()' function for getting predictions.


The constructor is the same as the constructor of the Task class, in addition to a path to where the model is saved.

The action() function of this task loads the model from the pickle file and returns its predictions.

The on_failure() function of this task guides the user why his action() function has failed.
In addition, you can access the model by Rest API, and get its predictions.
FilterColumnsTask
This task’s purpose is to filter unnecessary columns from your dataframe.

The constructor is the same as the constructor of the Task class, in addition to a list of column names to keep in the DataFrame.

The action() function of this task gets your dataframe and returns it after filtering it.

The on_failure() function of this task guides the user why his action() function has failed (why filtering the columns of the dataframe has failed)


FilterColumnsTask
This task’s purpose is to filter unnecessary rows from your dataframe.

The constructor is the same as the constructor of the Task class, in addition to a condition function that determines which rows to keep.

The action() function of this task gets your dataframe and returns it after filtering it.

The on_failure() function of this task guides the user why his action() function has failed (why filtering the rows of the dataframe has failed)


PostgresReaderTask
This task’s purpose is to read a table from postgres and turn it into a pandas dataframe. 

The constructor is the same as the constructor of the Task class, in addition to another parameter which is a dictionary which contains your connection details to the postgres.
The dictionary should contain the category of the connection detail (for example: username, password) as the key, and the value itself as the value of the key-value pair in the dictionary.

The action() function of this task connects to your postgres db, and returns a dataframe from the table you have chosen.

The on_failure() function of this task guides the user why his action() function has failed (why the connection to the postgres has failed)




Dag
A DAG (Directed Acyclic Graph) is a directed, non-circular graph which will describe the connections between the tasks.

The constructor contains a few parameters:
dag_id - The id of the dag.
name - The name of the dag.
start_condition - A start condition from the available start conditions of the library (time or trigger).
start_time - The time which the dag should start running.
tasks - A dictionary which contains a task as the key and list of all the tasks that depend on it as the value.
cache_type - A cache type from the available cache types of the library
exit_point_persistent - a boolean which defines if the output of the dag should be saved or not.

Furthermore, the class contains one other functions:
start_trigger()
This function defines the start trigger of the entire dag. It returns a tuple which contains the time which the dag should start running and a more specified start condition.

Moreover, you can import from groot.dag the function choice_options() .
This function allows you to choose the right option for you from the options that the library supports.





Convertor
This is an interface which allows you to convert objects. It only contains the function convert() .


AirflowConvertor
This class implements the interface Convertor, and it contains the function convert() , which allows you to convert objects to their counterparts in Airflow.


AirflowDagConverter
This class extends the AirflowConvertor class, and it allows you to convert a Dag to an Airflow’s Dag.
The constructor of this class receives an instance of Dag.

Additionally, the class contains the function convert() , which allows you to convert a Dag to an Airflow Dag, and the function get_python_task_by_id() which receives an id of a task and returns the requested task.


AirflowTaskConverter
This class extends the AirflowConvertor class, and it allows you to convert a Task to an Airflow’s Task.
The constructor of this class receives an instance of Task, the id of a Dag and the id of the dependent task.

Further the class contains the  function convert(), which creates a python operator from the convert_with_input() function



Deployer
This is an interface which allows you to deploy the Tasks and Dags. It only contains the function convert() , which deploys the target source and returns True on success or False on failure.


AirflowTaskDeployer
This class implements the interface Convertor,

The constructor receives a dag file path, a remote repo URL, and a local dags’ directory and initializes the Airflow_Deployer.

Moreover, it contains the function deploy() , which syncs the dag’s directory with git and copies the dag file into it, so that Airflow's LocalExecutor can detect and run it,
the function push_dag_to_git() , which gets a file path of a DAG file, copies it into the local repo directory, and pushes it to the remote git repository and the function create_dag_file() , 
which creates a pickle file and a dag file from the dag object and returns the path to the created dag file.


Client
This class allows you to use our library.
It contains the following functions:
create_dag()
The function prompts the user for all the required parameters and returns a configured Dag object which is ready to be deployed.

deploy()
The function gets a deployer and uses it to deploy the dag, returning True on success or False on failure.
	
convert()
The 'convert()' function gets a convertor and uses it to convert the dag to the required format.
