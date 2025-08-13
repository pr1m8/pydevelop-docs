testhaive.core.schema.state
===========================

.. py:module:: testhaive.core.schema.state

.. autoapi-nested-parse::

   State management schemas for agents and workflows.

   This module provides specialized state schemas for different types of stateful
   components in the testhaive framework, including agents, workflows, and execution contexts.



Classes
-------

.. autoapisummary::

   testhaive.core.schema.state.AgentState
   testhaive.core.schema.state.ExecutionContext
   testhaive.core.schema.state.ExecutionStatus
   testhaive.core.schema.state.ResourceType
   testhaive.core.schema.state.WorkflowState


Module Contents
---------------

.. py:class:: AgentState(**kwargs)

   Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


   State schema for individual agents.

   This schema tracks the complete state of an agent including its configuration,
   execution status, conversation history, tool usage, and performance metrics.

   .. attribute:: agent_name

      Name of the agent

   .. attribute:: agent_type

      Type/category of the agent

   .. attribute:: status

      Current execution status

   .. attribute:: conversation_history

      List of conversation messages

   .. attribute:: tool_calls

      List of tool calls made by the agent

   .. attribute:: current_task

      Description of current task being executed

   .. attribute:: task_queue

      Queue of pending tasks

   .. attribute:: error_messages

      List of error messages encountered

   .. attribute:: performance_metrics

      Performance tracking data

   .. attribute:: resource_usage

      Current resource utilization

   .. rubric:: Examples

   Creating an agent state::

       state = AgentState(
           agent_name="research_assistant",
           agent_type="react",
           status=ExecutionStatus.RUNNING,
           current_task="Analyzing research papers on AI safety"
       )

   Tracking conversation::

       state.add_conversation_message("user", "What are the main AI risks?")
       state.add_conversation_message("assistant", "The main risks include...")

   Recording tool usage::

       state.record_tool_call("web_search", {"query": "AI safety research"})
       state.record_tool_call("summarize", {"text": "Research paper content..."})

   Performance monitoring::

       state.update_performance_metric("response_time", 2.5)
       state.update_resource_usage(ResourceType.MEMORY, 1024.0)

   Initialize agent state with proper state type.


   .. py:method:: add_conversation_message(role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None

      Add a message to the conversation history.

      :param role: Role of the message sender (user, assistant, system)
      :param content: Content of the message
      :param metadata: Optional metadata for the message



   .. py:method:: add_error(error_message: str) -> None

      Add an error message to the error log.

      :param error_message: Error message to record



   .. py:method:: add_task_to_queue(task_description: str) -> None

      Add a task to the pending task queue.

      :param task_description: Description of the task to add



   .. py:method:: complete_current_task() -> Optional[str]

      Complete the current task and move to next in queue.

      :returns: Next task from queue if available, None otherwise



   .. py:method:: get_conversation_summary() -> Dict[str, Any]

      Get a summary of the conversation history.

      :returns: Dictionary with conversation statistics



   .. py:method:: get_tool_usage_summary() -> Dict[str, Any]

      Get a summary of tool usage.

      :returns: Dictionary with tool usage statistics



   .. py:method:: record_tool_call(tool_name: str, parameters: Dict[str, Any], result: Optional[Any] = None) -> None

      Record a tool call made by the agent.

      :param tool_name: Name of the tool called
      :param parameters: Parameters passed to the tool
      :param result: Result returned by the tool (if available)



   .. py:method:: set_current_task(task_description: str) -> None

      Set the current task being executed.

      :param task_description: Description of the task



   .. py:method:: update_performance_metric(metric_name: str, value: float) -> None

      Update a performance metric.

      :param metric_name: Name of the metric
      :param value: New value for the metric



   .. py:method:: update_resource_usage(resource_type: ResourceType, usage: float) -> None

      Update resource usage tracking.

      :param resource_type: Type of resource being tracked
      :param usage: Current usage amount



   .. py:attribute:: agent_name
      :type:  str
      :value: None



   .. py:attribute:: agent_type
      :type:  str
      :value: None



   .. py:attribute:: conversation_history
      :type:  List[Dict[str, Any]]
      :value: None



   .. py:attribute:: current_task
      :type:  Optional[str]
      :value: None



   .. py:attribute:: error_messages
      :type:  List[str]
      :value: None



   .. py:attribute:: performance_metrics
      :type:  Dict[str, float]
      :value: None



   .. py:attribute:: resource_usage
      :type:  Dict[str, float]
      :value: None



   .. py:attribute:: status
      :type:  ExecutionStatus
      :value: None



   .. py:attribute:: task_queue
      :type:  List[str]
      :value: None



   .. py:attribute:: tool_calls
      :type:  List[Dict[str, Any]]
      :value: None



.. py:class:: ExecutionContext(**kwargs)

   Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


   Execution context schema for tracking runtime environments.

   This schema captures the complete execution environment including system resources,
   configuration parameters, environment variables, and runtime constraints.

   .. attribute:: context_name

      Name of the execution context

   .. attribute:: environment

      Environment name (dev, staging, prod)

   .. attribute:: system_info

      System information and capabilities

   .. attribute:: resource_limits

      Resource usage limits

   .. attribute:: environment_variables

      Environment variable settings

   .. attribute:: execution_parameters

      Runtime execution parameters

   .. attribute:: active_sessions

      Currently active execution sessions

   .. attribute:: monitoring_data

      Performance and health monitoring data

   .. rubric:: Examples

   Creating an execution context::

       context = ExecutionContext(
           context_name="production_environment",
           environment="prod",
           resource_limits={"max_memory": 8192, "max_cpu": 80}
       )

   Managing sessions::

       session_id = context.start_execution_session("data_pipeline")
       context.update_session_status(session_id, ExecutionStatus.RUNNING)
       context.end_execution_session(session_id, {"processed_records": 1000})

   Resource monitoring::

       context.update_monitoring_data("cpu_usage", 45.2)
       context.update_monitoring_data("memory_usage", 2048.0)
       context.check_resource_limits()

   Initialize execution context with proper state type.


   .. py:method:: check_resource_limits() -> Dict[str, bool]

      Check if current resource usage is within limits.

      :returns: Dictionary showing which limits are exceeded



   .. py:method:: end_execution_session(session_id: str, outputs: Optional[Dict[str, Any]] = None) -> None

      End an execution session.

      :param session_id: ID of the session to end
      :param outputs: Optional session outputs



   .. py:method:: get_session_summary() -> Dict[str, Any]

      Get a summary of execution sessions.

      :returns: Dictionary with session statistics



   .. py:method:: start_execution_session(session_name: str, parameters: Optional[Dict[str, Any]] = None) -> str

      Start a new execution session.

      :param session_name: Name/description of the session
      :param parameters: Optional session parameters

      :returns: Unique session ID



   .. py:method:: update_monitoring_data(metric_name: str, value: float) -> None

      Update monitoring data with a new metric value.

      :param metric_name: Name of the metric
      :param value: New metric value



   .. py:method:: update_session_status(session_id: str, status: ExecutionStatus) -> None

      Update the status of an execution session.

      :param session_id: ID of the session to update
      :param status: New status for the session



   .. py:attribute:: active_sessions
      :type:  Dict[str, Dict[str, Any]]
      :value: None



   .. py:attribute:: context_name
      :type:  str
      :value: None



   .. py:attribute:: environment
      :type:  str
      :value: None



   .. py:attribute:: environment_variables
      :type:  Dict[str, str]
      :value: None



   .. py:attribute:: execution_parameters
      :type:  Dict[str, Any]
      :value: None



   .. py:attribute:: monitoring_data
      :type:  Dict[str, List[Tuple[datetime.datetime, float]]]
      :value: None



   .. py:attribute:: resource_limits
      :type:  Dict[str, float]
      :value: None



   .. py:attribute:: system_info
      :type:  Dict[str, Any]
      :value: None



.. py:class:: ExecutionStatus

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Status values for execution tracking.

   .. attribute:: PENDING

      Execution is pending/queued

   .. attribute:: RUNNING

      Currently executing

   .. attribute:: COMPLETED

      Execution completed successfully

   .. attribute:: FAILED

      Execution failed with errors

   .. attribute:: CANCELLED

      Execution was cancelled

   .. attribute:: TIMEOUT

      Execution timed out

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: CANCELLED
      :value: 'cancelled'



   .. py:attribute:: COMPLETED
      :value: 'completed'



   .. py:attribute:: FAILED
      :value: 'failed'



   .. py:attribute:: PENDING
      :value: 'pending'



   .. py:attribute:: RUNNING
      :value: 'running'



   .. py:attribute:: TIMEOUT
      :value: 'timeout'



.. py:class:: ResourceType

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Types of resources that can be tracked.

   .. attribute:: MEMORY

      Memory/RAM usage

   .. attribute:: CPU

      CPU utilization

   .. attribute:: DISK

      Disk space usage

   .. attribute:: NETWORK

      Network bandwidth

   .. attribute:: GPU

      GPU utilization

   .. attribute:: CUSTOM

      Custom resource type

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: CPU
      :value: 'cpu'



   .. py:attribute:: CUSTOM
      :value: 'custom'



   .. py:attribute:: DISK
      :value: 'disk'



   .. py:attribute:: GPU
      :value: 'gpu'



   .. py:attribute:: MEMORY
      :value: 'memory'



   .. py:attribute:: NETWORK
      :value: 'network'



.. py:class:: WorkflowState(**kwargs)

   Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


   State schema for workflow execution tracking.

   This schema manages the state of multi-step workflows, including step execution,
   dependencies, parallel processing, and error recovery.

   .. attribute:: workflow_name

      Name of the workflow

   .. attribute:: workflow_version

      Version of the workflow definition

   .. attribute:: steps

      List of workflow steps with their states

   .. attribute:: current_step_index

      Index of currently executing step

   .. attribute:: completed_steps

      Set of completed step IDs

   .. attribute:: failed_steps

      Set of failed step IDs

   .. attribute:: parallel_branches

      Active parallel execution branches

   .. attribute:: workflow_inputs

      Initial inputs to the workflow

   .. attribute:: workflow_outputs

      Final outputs from the workflow

   .. attribute:: step_dependencies

      Dependencies between workflow steps

   .. rubric:: Examples

   Creating a workflow state::

       workflow = WorkflowState(
           workflow_name="data_processing_pipeline",
           workflow_version="1.2.0",
           workflow_inputs={"data_source": "database", "batch_size": 1000}
       )

   Managing workflow steps::

       workflow.add_step("extract_data", {"source": "database"})
       workflow.add_step("transform_data", {"rules": "clean_nulls"})
       workflow.add_step("load_data", {"destination": "warehouse"})

   Executing workflow::

       workflow.start_step("extract_data")
       # ... step execution ...
       workflow.complete_step("extract_data", {"records_extracted": 5000})

   Handling dependencies::

       workflow.add_step_dependency("transform_data", "extract_data")
       workflow.add_step_dependency("load_data", "transform_data")

   Initialize workflow state with proper state type.


   .. py:method:: add_step(step_id: str, step_config: Dict[str, Any]) -> None

      Add a step to the workflow.

      :param step_id: Unique identifier for the step
      :param step_config: Configuration for the step



   .. py:method:: add_step_dependency(step_id: str, depends_on: str) -> None

      Add a dependency relationship between steps.

      :param step_id: ID of the step that has a dependency
      :param depends_on: ID of the step that must complete first



   .. py:method:: can_execute_step(step_id: str) -> bool

      Check if a step can be executed based on dependencies.

      :param step_id: ID of the step to check

      :returns: True if step can be executed, False otherwise



   .. py:method:: complete_step(step_id: str, outputs: Dict[str, Any]) -> None

      Mark a workflow step as completed.

      :param step_id: ID of the completed step
      :param outputs: Outputs produced by the step



   .. py:method:: fail_step(step_id: str, error_message: str) -> None

      Mark a workflow step as failed.

      :param step_id: ID of the failed step
      :param error_message: Error message describing the failure



   .. py:method:: get_executable_steps() -> List[str]

      Get list of steps that can currently be executed.

      :returns: List of step IDs that can be executed



   .. py:method:: get_workflow_progress() -> Dict[str, Any]

      Get overall workflow progress information.

      :returns: Dictionary with progress statistics



   .. py:method:: start_step(step_id: str) -> bool

      Start execution of a workflow step.

      :param step_id: ID of the step to start

      :returns: True if step was started, False if dependencies not met



   .. py:attribute:: completed_steps
      :type:  Set[str]
      :value: None



   .. py:attribute:: current_step_index
      :type:  int
      :value: None



   .. py:attribute:: failed_steps
      :type:  Set[str]
      :value: None



   .. py:attribute:: parallel_branches
      :type:  Dict[str, List[str]]
      :value: None



   .. py:attribute:: step_dependencies
      :type:  Dict[str, List[str]]
      :value: None



   .. py:attribute:: steps
      :type:  List[Dict[str, Any]]
      :value: None



   .. py:attribute:: workflow_inputs
      :type:  Dict[str, Any]
      :value: None



   .. py:attribute:: workflow_name
      :type:  str
      :value: None



   .. py:attribute:: workflow_outputs
      :type:  Dict[str, Any]
      :value: None



   .. py:attribute:: workflow_version
      :type:  str
      :value: None



