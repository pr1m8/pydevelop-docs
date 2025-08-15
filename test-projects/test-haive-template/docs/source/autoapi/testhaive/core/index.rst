testhaive.core
==============

.. py:module:: testhaive.core

TestHaive Core - Core framework components.

This package mimics the structure of haive.core for testing documentation generation.


.. autolink-examples:: testhaive.core
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">5 classes</span>   </div>

.. autoapi-nested-parse::

   TestHaive Core - Core framework components.

   This package mimics the structure of haive.core for testing documentation generation.


   .. autolink-examples:: testhaive.core
      :collapse:



.. admonition:: Submodules (3)
   :class: note

   .. toctree::
      :maxdepth: 1
      :titlesonly:

      /autoapi/testhaive/core/engine/index
      /autoapi/testhaive/core/schema/index
      /autoapi/testhaive/core/tools/index

      
            
            

.. admonition:: Classes (5)
   :class: note

   .. autoapisummary::

      testhaive.core.BaseSchema
      testhaive.core.BaseTool
      testhaive.core.EngineMode
      testhaive.core.StateSchema
      testhaive.core.TestLLMConfig

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

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

.. py:class:: BaseTool(/, **data: Any)

            Bases: :py:obj:`pydantic.BaseModel`


            Base class for all tools in testhaive framework.

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: BaseTool
               :collapse:

            .. py:method:: execute(**kwargs) -> Dict[str, Any]

               Execute the tool with given parameters.


               .. autolink-examples:: execute
                  :collapse:


            .. py:attribute:: description
               :type:  str
               :value: None



            .. py:attribute:: name
               :type:  str
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: EngineMode

            Bases: :py:obj:`str`, :py:obj:`enum.Enum`


            Engine execution modes (mimics Haive's patterns).

            Initialize self.  See help(type(self)) for accurate signature.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: EngineMode
               :collapse:

            .. py:attribute:: MULTI_AGENT
               :value: 'multi_agent'



            .. py:attribute:: REACT
               :value: 'react'



            .. py:attribute:: SIMPLE
               :value: 'simple'



            .. py:attribute:: STREAMING
               :value: 'streaming'




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

.. py:class:: TestLLMConfig(/, **data: Any)

            Bases: :py:obj:`pydantic.BaseModel`


            Main LLM configuration class (mimics AugLLMConfig).

            This class mimics the complexity and patterns of AugLLMConfig.

            :param name: Configuration name
            :param model: LLM model identifier
            :param mode: Engine execution mode
            :param temperature: Sampling temperature (0.0-2.0)
            :param max_tokens: Maximum output tokens
            :param tools: List of available tools
            :param system_message: System prompt
            :param metadata: Additional configuration metadata

            .. rubric:: Examples

            Basic configuration::

                config = TestLLMConfig(
                    name="simple_config",
                    model="gpt-4",
                    mode=EngineMode.SIMPLE,
                    temperature=0.7
                )

            React agent configuration::

                config = TestLLMConfig(
                    name="react_config",
                    model="gpt-4",
                    mode=EngineMode.REACT,
                    temperature=0.3,
                    max_tokens=1000,
                    tools=["calculator", "search"],
                    system_message="You are a helpful assistant."
                )

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: TestLLMConfig
               :collapse:

            .. py:method:: add_tool(tool_name: str) -> None

               Add a tool to the configuration.

               :param tool_name: Name of the tool to add


               .. autolink-examples:: add_tool
                  :collapse:


            .. py:method:: get_summary() -> Dict[str, Any]

               Get configuration summary.

               :returns: Dictionary containing configuration summary


               .. autolink-examples:: get_summary
                  :collapse:


            .. py:method:: remove_tool(tool_name: str) -> None

               Remove a tool from the configuration.

               :param tool_name: Name of the tool to remove


               .. autolink-examples:: remove_tool
                  :collapse:


            .. py:method:: with_tools(tools: List[str]) -> TestLLMConfig

               Create a new config with specified tools.

               :param tools: List of tool names

               :returns: New TestLLMConfig instance with tools


               .. autolink-examples:: with_tools
                  :collapse:


            .. py:attribute:: max_tokens
               :type:  Optional[int]
               :value: None



            .. py:attribute:: metadata
               :type:  Dict[str, Any]
               :value: None



            .. py:attribute:: mode
               :type:  EngineMode
               :value: None



            .. py:attribute:: model
               :type:  str
               :value: None



            .. py:attribute:: name
               :type:  str
               :value: None



            .. py:attribute:: system_message
               :type:  Optional[str]
               :value: None



            .. py:attribute:: temperature
               :type:  float
               :value: None



            .. py:attribute:: tools
               :type:  List[str]
               :value: None






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.core import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

