testhaive.core.schema
=====================

.. py:module:: testhaive.core.schema

Schema module for testhaive.core data structures and state management.


.. autolink-examples:: testhaive.core.schema
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">9 classes</span>   </div>

.. autoapi-nested-parse::

   Schema module for testhaive.core data structures and state management.


   .. autolink-examples:: testhaive.core.schema
      :collapse:



.. admonition:: Submodules (3)
   :class: note

   .. toctree::
      :maxdepth: 1
      :titlesonly:

      /autoapi/testhaive/core/schema/base/index
      /autoapi/testhaive/core/schema/meta/index
      /autoapi/testhaive/core/schema/state/index

      
            
            

.. admonition:: Classes (9)
   :class: note

   .. autoapisummary::

      testhaive.core.schema.AgentState
      testhaive.core.schema.BaseSchema
      testhaive.core.schema.ExecutionContext
      testhaive.core.schema.MetaStateSchema
      testhaive.core.schema.StateProjection
      testhaive.core.schema.StateSchema
      testhaive.core.schema.StateTransfer
      testhaive.core.schema.ValidationMixin
      testhaive.core.schema.WorkflowState

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

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


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: AgentState
               :collapse:

            .. py:method:: add_conversation_message(role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None

               Add a message to the conversation history.

               :param role: Role of the message sender (user, assistant, system)
               :param content: Content of the message
               :param metadata: Optional metadata for the message


               .. autolink-examples:: add_conversation_message
                  :collapse:


            .. py:method:: add_error(error_message: str) -> None

               Add an error message to the error log.

               :param error_message: Error message to record


               .. autolink-examples:: add_error
                  :collapse:


            .. py:method:: add_task_to_queue(task_description: str) -> None

               Add a task to the pending task queue.

               :param task_description: Description of the task to add


               .. autolink-examples:: add_task_to_queue
                  :collapse:


            .. py:method:: complete_current_task() -> Optional[str]

               Complete the current task and move to next in queue.

               :returns: Next task from queue if available, None otherwise


               .. autolink-examples:: complete_current_task
                  :collapse:


            .. py:method:: get_conversation_summary() -> Dict[str, Any]

               Get a summary of the conversation history.

               :returns: Dictionary with conversation statistics


               .. autolink-examples:: get_conversation_summary
                  :collapse:


            .. py:method:: get_tool_usage_summary() -> Dict[str, Any]

               Get a summary of tool usage.

               :returns: Dictionary with tool usage statistics


               .. autolink-examples:: get_tool_usage_summary
                  :collapse:


            .. py:method:: record_tool_call(tool_name: str, parameters: Dict[str, Any], result: Optional[Any] = None) -> None

               Record a tool call made by the agent.

               :param tool_name: Name of the tool called
               :param parameters: Parameters passed to the tool
               :param result: Result returned by the tool (if available)


               .. autolink-examples:: record_tool_call
                  :collapse:


            .. py:method:: set_current_task(task_description: str) -> None

               Set the current task being executed.

               :param task_description: Description of the task


               .. autolink-examples:: set_current_task
                  :collapse:


            .. py:method:: update_performance_metric(metric_name: str, value: float) -> None

               Update a performance metric.

               :param metric_name: Name of the metric
               :param value: New value for the metric


               .. autolink-examples:: update_performance_metric
                  :collapse:


            .. py:method:: update_resource_usage(resource_type: ResourceType, usage: float) -> None

               Update resource usage tracking.

               :param resource_type: Type of resource being tracked
               :param usage: Current usage amount


               .. autolink-examples:: update_resource_usage
                  :collapse:


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




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: BaseSchema(**kwargs)

            Bases: :py:obj:`pydantic.BaseModel`, :py:obj:`ValidationMixin`


            Base schema class for all testhaive schemas.

            This is the foundational schema class that provides common functionality
            including validation, serialization, metadata tracking, and lifecycle management.
            All other schemas in the testhaive framework should inherit from this class.

            .. attribute:: created_at

               Timestamp when schema was created

            .. attribute:: updated_at

               Timestamp when schema was last updated

            .. attribute:: version

               Schema version for compatibility tracking

            .. attribute:: metadata

               Additional metadata dictionary

            .. rubric:: Examples

            Basic usage::

                class UserSchema(BaseSchema):
                    name: str
                    email: str
                    age: int

                user = UserSchema(
                    name="John Doe",
                    email="john@example.com",
                    age=30
                )

            With custom metadata::

                user = UserSchema(
                    name="Jane Smith",
                    email="jane@example.com",
                    age=25,
                    metadata={"department": "engineering", "role": "senior"}
                )

            Serialization example::

                # Export to JSON
                json_data = user.serialize(SerializationFormat.JSON)

                # Export to dictionary
                dict_data = user.serialize(SerializationFormat.DICT)

                # Load from data
                restored_user = UserSchema.deserialize(json_data, SerializationFormat.JSON)

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: BaseSchema
               :collapse:

            .. py:class:: Config

               Pydantic configuration for BaseSchema.


               .. autolink-examples:: Config
                  :collapse:

               .. py:attribute:: extra
                  :value: 'forbid'



               .. py:attribute:: json_encoders


               .. py:attribute:: use_enum_values
                  :value: True



               .. py:attribute:: validate_assignment
                  :value: True




            .. py:method:: _validate_business_rules() -> None

               Validate business logic rules.


               .. autolink-examples:: _validate_business_rules
                  :collapse:


            .. py:method:: _validate_fields() -> None

               Validate individual field constraints.


               .. autolink-examples:: _validate_fields
                  :collapse:


            .. py:method:: _validate_relationships() -> None

               Validate relationships between fields.


               .. autolink-examples:: _validate_relationships
                  :collapse:


            .. py:method:: deserialize(data: Union[str, Dict[str, Any], bytes], format: SerializationFormat = SerializationFormat.JSON) -> T
               :classmethod:


               Deserialize data to create schema instance.

               :param data: Data to deserialize
               :param format: Format of the input data

               :returns: New schema instance created from data

               :raises ValueError: If format is not supported or data is invalid

               .. rubric:: Examples

               From JSON string::

                   schema = MySchema.deserialize(json_str, SerializationFormat.JSON)

               From dictionary::

                   schema = MySchema.deserialize(data_dict, SerializationFormat.DICT)


               .. autolink-examples:: deserialize
                  :collapse:


            .. py:method:: get_metadata(key: str, default: Any = None) -> Any

               Get a metadata value.

               :param key: Metadata key
               :param default: Default value if key not found

               :returns: Metadata value or default


               .. autolink-examples:: get_metadata
                  :collapse:


            .. py:method:: get_schema_info() -> Dict[str, Any]

               Get schema information summary.

               :returns: Dictionary containing schema metadata and status


               .. autolink-examples:: get_schema_info
                  :collapse:


            .. py:method:: serialize(format: SerializationFormat = SerializationFormat.JSON) -> Union[str, Dict[str, Any], bytes]

               Serialize schema to specified format.

               :param format: Serialization format to use

               :returns: Serialized data in the specified format

               :raises ValueError: If format is not supported

               .. rubric:: Examples

               JSON serialization::

                   json_str = schema.serialize(SerializationFormat.JSON)

               Dictionary serialization::

                   data_dict = schema.serialize(SerializationFormat.DICT)


               .. autolink-examples:: serialize
                  :collapse:


            .. py:method:: set_metadata(key: str, value: Any) -> None

               Set a metadata value.

               :param key: Metadata key
               :param value: Metadata value


               .. autolink-examples:: set_metadata
                  :collapse:


            .. py:method:: update_timestamp() -> None

               Update the updated_at timestamp to current time.


               .. autolink-examples:: update_timestamp
                  :collapse:


            .. py:method:: validate_all() -> bool

               Validate all fields and relationships.

               Performs comprehensive validation including:
               - Field type validation
               - Value range validation
               - Cross-field relationship validation
               - Business logic validation

               :returns: True if validation passes, False otherwise

               .. rubric:: Examples

               Basic validation::

                   if not schema.validate_all():
                       errors = schema.get_validation_errors()
                       print(f"Validation failed: {errors}")

               With different validation levels::

                   schema.set_validation_level(ValidationLevel.STRICT)
                   is_valid = schema.validate_all()


               .. autolink-examples:: validate_all
                  :collapse:


            .. py:attribute:: created_at
               :type:  datetime.datetime
               :value: None



            .. py:attribute:: metadata
               :type:  Dict[str, Any]
               :value: None



            .. py:attribute:: updated_at
               :type:  datetime.datetime
               :value: None



            .. py:attribute:: version
               :type:  str
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

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


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ExecutionContext
               :collapse:

            .. py:method:: check_resource_limits() -> Dict[str, bool]

               Check if current resource usage is within limits.

               :returns: Dictionary showing which limits are exceeded


               .. autolink-examples:: check_resource_limits
                  :collapse:


            .. py:method:: end_execution_session(session_id: str, outputs: Optional[Dict[str, Any]] = None) -> None

               End an execution session.

               :param session_id: ID of the session to end
               :param outputs: Optional session outputs


               .. autolink-examples:: end_execution_session
                  :collapse:


            .. py:method:: get_session_summary() -> Dict[str, Any]

               Get a summary of execution sessions.

               :returns: Dictionary with session statistics


               .. autolink-examples:: get_session_summary
                  :collapse:


            .. py:method:: start_execution_session(session_name: str, parameters: Optional[Dict[str, Any]] = None) -> str

               Start a new execution session.

               :param session_name: Name/description of the session
               :param parameters: Optional session parameters

               :returns: Unique session ID


               .. autolink-examples:: start_execution_session
                  :collapse:


            .. py:method:: update_monitoring_data(metric_name: str, value: float) -> None

               Update monitoring data with a new metric value.

               :param metric_name: Name of the metric
               :param value: New metric value


               .. autolink-examples:: update_monitoring_data
                  :collapse:


            .. py:method:: update_session_status(session_id: str, status: ExecutionStatus) -> None

               Update the status of an execution session.

               :param session_id: ID of the session to update
               :param status: New status for the session


               .. autolink-examples:: update_session_status
                  :collapse:


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




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: MetaStateSchema(**kwargs)

            Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


            Meta-state schema for complex state projections.

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: MetaStateSchema
               :collapse:

            .. py:attribute:: agent_states
               :type:  Dict[str, Dict[str, Any]]
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: StateProjection(**kwargs)

            Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


            State projection for filtered views.

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: StateProjection
               :collapse:

            .. py:attribute:: projection_fields
               :type:  List[str]
               :value: None



            .. py:attribute:: source_state_id
               :type:  str
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: StateSchema(**kwargs)

            Bases: :py:obj:`BaseSchema`


            Base class for all state schemas in the testhaive framework.

            StateSchema extends BaseSchema with state-specific functionality including
            state transitions, history tracking, rollback capabilities, and state validation.

            This class is designed for schemas that represent mutable state that changes
            over time, such as agent states, workflow states, and execution contexts.

            .. attribute:: state_id

               Unique identifier for this state instance

            .. attribute:: previous_state_id

               ID of the previous state in the chain

            .. attribute:: state_type

               Type classification for this state

            .. attribute:: is_final

               Whether this is a final/terminal state

            .. attribute:: transition_count

               Number of transitions this state has undergone

            .. rubric:: Examples

            Basic state schema::

                class GameState(StateSchema):
                    player_position: Tuple[int, int]
                    score: int
                    level: int

                state = GameState(
                    player_position=(0, 0),
                    score=0,
                    level=1,
                    state_type="game"
                )

            State transitions::

                # Create new state from current
                new_state = state.create_transition(
                    player_position=(1, 0),
                    score=100
                )

                # Rollback to previous state
                if new_state.can_rollback():
                    previous = new_state.rollback()

            State history tracking::

                # Get transition history
                history = state.get_transition_history()

                # Check if state has changed
                if state.has_changed_since(previous_state_id):
                    print("State has been modified")

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: StateSchema
               :collapse:

            .. py:method:: can_rollback() -> bool

               Check if this state can be rolled back to its previous state.

               :returns: True if rollback is possible, False otherwise


               .. autolink-examples:: can_rollback
                  :collapse:


            .. py:method:: create_transition(**changes) -> T

               Create a new state instance with the specified changes.

               This method creates a new state that inherits from the current state
               but with the specified field changes applied. The new state will
               reference this state as its previous state.

               :param \*\*changes: Field changes to apply to the new state

               :returns: New state instance with changes applied

               .. rubric:: Examples

               Simple field update::

                   new_state = current_state.create_transition(score=150)

               Multiple field changes::

                   new_state = current_state.create_transition(
                       player_position=(2, 3),
                       score=200,
                       level=2
                   )


               .. autolink-examples:: create_transition
                  :collapse:


            .. py:method:: get_state_summary() -> Dict[str, Any]

               Get a summary of this state's information.

               :returns: Dictionary containing state summary information


               .. autolink-examples:: get_state_summary
                  :collapse:


            .. py:method:: get_transition_history() -> List[str]

               Get the history of state transitions.

               :returns: List of state IDs in the transition chain

               .. note::

                  This method only returns the current state ID. In a real implementation,
                  this would traverse the state chain to build the complete history.


               .. autolink-examples:: get_transition_history
                  :collapse:


            .. py:method:: has_changed_since(state_id: str) -> bool

               Check if this state has changed since the specified state.

               :param state_id: ID of the state to compare against

               :returns: True if state has changed, False otherwise


               .. autolink-examples:: has_changed_since
                  :collapse:


            .. py:method:: mark_final() -> None

               Mark this state as final/terminal.

               Final states cannot be transitioned from or rolled back.


               .. autolink-examples:: mark_final
                  :collapse:


            .. py:method:: rollback() -> Optional[StateSchema]

               Attempt to rollback to the previous state.

               .. note::

                  This method returns None as it cannot reconstruct the previous state
                  without access to a state store. In a real implementation, this would
                  query a state repository to retrieve the previous state.

               :returns: Previous state instance if available, None otherwise

               :raises ValueError: If rollback is not possible


               .. autolink-examples:: rollback
                  :collapse:


            .. py:attribute:: is_final
               :type:  bool
               :value: None



            .. py:attribute:: previous_state_id
               :type:  Optional[str]
               :value: None



            .. py:attribute:: state_id
               :type:  str
               :value: None



            .. py:attribute:: state_type
               :type:  str
               :value: None



            .. py:attribute:: transition_count
               :type:  int
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: StateTransfer(**kwargs)

            Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


            State transfer configuration.

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: StateTransfer
               :collapse:

            .. py:attribute:: source_agent
               :type:  str
               :value: None



            .. py:attribute:: target_agent
               :type:  str
               :value: None



            .. py:attribute:: transfer_rules
               :type:  Dict[str, str]
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ValidationMixin(*args, **kwargs)

            Bases: :py:obj:`abc.ABC`


            Mixin class providing validation capabilities to schemas.

            This mixin adds comprehensive validation functionality including custom validators,
            field-level validation, cross-field validation, and validation reporting.

            .. rubric:: Examples

            Using validation mixin::

                class MySchema(BaseSchema, ValidationMixin):
                    name: str
                    age: int

                    def validate_age(self, value: int) -> int:
                        if value < 0:
                            raise ValueError("Age cannot be negative")
                        return value

            Custom validation levels::

                schema = MySchema(name="test", age=25)
                schema.set_validation_level(ValidationLevel.STRICT)
                result = schema.validate_all()

            Initialize validation mixin with default settings.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ValidationMixin
               :collapse:

            .. py:method:: add_validation_error(message: str) -> None

               Add a validation error message.

               :param message: Error message to add


               .. autolink-examples:: add_validation_error
                  :collapse:


            .. py:method:: add_validation_warning(message: str) -> None

               Add a validation warning message.

               :param message: Warning message to add


               .. autolink-examples:: add_validation_warning
                  :collapse:


            .. py:method:: clear_validation_messages() -> None

               Clear all validation errors and warnings.


               .. autolink-examples:: clear_validation_messages
                  :collapse:


            .. py:method:: get_validation_errors() -> List[str]

               Get list of validation errors.

               :returns: List of validation error messages


               .. autolink-examples:: get_validation_errors
                  :collapse:


            .. py:method:: get_validation_warnings() -> List[str]

               Get list of validation warnings.

               :returns: List of validation warning messages


               .. autolink-examples:: get_validation_warnings
                  :collapse:


            .. py:method:: set_validation_level(level: ValidationLevel) -> None

               Set the validation level for this schema.

               :param level: Validation level to use

               .. rubric:: Examples

               Setting strict validation::

                   schema.set_validation_level(ValidationLevel.STRICT)

               Disabling validation for performance::

                   schema.set_validation_level(ValidationLevel.DISABLED)


               .. autolink-examples:: set_validation_level
                  :collapse:


            .. py:method:: validate_all() -> bool
               :abstractmethod:


               Validate all fields and relationships.

               :returns: True if validation passes, False otherwise

               .. note:: Subclasses must implement this method to define their validation logic.


               .. autolink-examples:: validate_all
                  :collapse:


            .. py:attribute:: _validation_errors
               :type:  List[str]
               :value: []



            .. py:attribute:: _validation_level


            .. py:attribute:: _validation_warnings
               :type:  List[str]
               :value: []




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

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


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: WorkflowState
               :collapse:

            .. py:method:: add_step(step_id: str, step_config: Dict[str, Any]) -> None

               Add a step to the workflow.

               :param step_id: Unique identifier for the step
               :param step_config: Configuration for the step


               .. autolink-examples:: add_step
                  :collapse:


            .. py:method:: add_step_dependency(step_id: str, depends_on: str) -> None

               Add a dependency relationship between steps.

               :param step_id: ID of the step that has a dependency
               :param depends_on: ID of the step that must complete first


               .. autolink-examples:: add_step_dependency
                  :collapse:


            .. py:method:: can_execute_step(step_id: str) -> bool

               Check if a step can be executed based on dependencies.

               :param step_id: ID of the step to check

               :returns: True if step can be executed, False otherwise


               .. autolink-examples:: can_execute_step
                  :collapse:


            .. py:method:: complete_step(step_id: str, outputs: Dict[str, Any]) -> None

               Mark a workflow step as completed.

               :param step_id: ID of the completed step
               :param outputs: Outputs produced by the step


               .. autolink-examples:: complete_step
                  :collapse:


            .. py:method:: fail_step(step_id: str, error_message: str) -> None

               Mark a workflow step as failed.

               :param step_id: ID of the failed step
               :param error_message: Error message describing the failure


               .. autolink-examples:: fail_step
                  :collapse:


            .. py:method:: get_executable_steps() -> List[str]

               Get list of steps that can currently be executed.

               :returns: List of step IDs that can be executed


               .. autolink-examples:: get_executable_steps
                  :collapse:


            .. py:method:: get_workflow_progress() -> Dict[str, Any]

               Get overall workflow progress information.

               :returns: Dictionary with progress statistics


               .. autolink-examples:: get_workflow_progress
                  :collapse:


            .. py:method:: start_step(step_id: str) -> bool

               Start execution of a workflow step.

               :param step_id: ID of the step to start

               :returns: True if step was started, False if dependencies not met


               .. autolink-examples:: start_step
                  :collapse:


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






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.core.schema import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

