"""State management schemas for agents and workflows.

This module provides specialized state schemas for different types of stateful
components in the testhaive framework, including agents, workflows, and execution contexts.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from pydantic import Field, validator

from .base import StateSchema, ValidationLevel


class ExecutionStatus(str, Enum):
    """Status values for execution tracking.

    Attributes:
        PENDING: Execution is pending/queued
        RUNNING: Currently executing
        COMPLETED: Execution completed successfully
        FAILED: Execution failed with errors
        CANCELLED: Execution was cancelled
        TIMEOUT: Execution timed out
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ResourceType(str, Enum):
    """Types of resources that can be tracked.

    Attributes:
        MEMORY: Memory/RAM usage
        CPU: CPU utilization
        DISK: Disk space usage
        NETWORK: Network bandwidth
        GPU: GPU utilization
        CUSTOM: Custom resource type
    """

    MEMORY = "memory"
    CPU = "cpu"
    DISK = "disk"
    NETWORK = "network"
    GPU = "gpu"
    CUSTOM = "custom"


class AgentState(StateSchema):
    """State schema for individual agents.

    This schema tracks the complete state of an agent including its configuration,
    execution status, conversation history, tool usage, and performance metrics.

    Attributes:
        agent_name: Name of the agent
        agent_type: Type/category of the agent
        status: Current execution status
        conversation_history: List of conversation messages
        tool_calls: List of tool calls made by the agent
        current_task: Description of current task being executed
        task_queue: Queue of pending tasks
        error_messages: List of error messages encountered
        performance_metrics: Performance tracking data
        resource_usage: Current resource utilization

    Examples:
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
    """

    agent_name: str = Field(..., description="Name of the agent")
    agent_type: str = Field(..., description="Type/category of the agent")
    status: ExecutionStatus = Field(
        default=ExecutionStatus.PENDING, description="Current execution status"
    )
    conversation_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of conversation messages"
    )
    tool_calls: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of tool calls made by the agent"
    )
    current_task: Optional[str] = Field(
        default=None, description="Description of current task being executed"
    )
    task_queue: List[str] = Field(
        default_factory=list, description="Queue of pending tasks"
    )
    error_messages: List[str] = Field(
        default_factory=list, description="List of error messages encountered"
    )
    performance_metrics: Dict[str, float] = Field(
        default_factory=dict, description="Performance tracking data"
    )
    resource_usage: Dict[str, float] = Field(
        default_factory=dict, description="Current resource utilization"
    )

    def __init__(self, **kwargs):
        """Initialize agent state with proper state type."""
        kwargs.setdefault("state_type", "agent")
        super().__init__(**kwargs)

    def add_conversation_message(
        self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a message to the conversation history.

        Args:
            role: Role of the message sender (user, assistant, system)
            content: Content of the message
            metadata: Optional metadata for the message
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        self.conversation_history.append(message)
        self.update_timestamp()

    def record_tool_call(
        self, tool_name: str, parameters: Dict[str, Any], result: Optional[Any] = None
    ) -> None:
        """Record a tool call made by the agent.

        Args:
            tool_name: Name of the tool called
            parameters: Parameters passed to the tool
            result: Result returned by the tool (if available)
        """
        tool_call = {
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "call_id": f"call_{len(self.tool_calls) + 1}",
        }
        self.tool_calls.append(tool_call)
        self.update_timestamp()

    def set_current_task(self, task_description: str) -> None:
        """Set the current task being executed.

        Args:
            task_description: Description of the task
        """
        self.current_task = task_description
        self.status = ExecutionStatus.RUNNING
        self.update_timestamp()

    def add_task_to_queue(self, task_description: str) -> None:
        """Add a task to the pending task queue.

        Args:
            task_description: Description of the task to add
        """
        self.task_queue.append(task_description)
        self.update_timestamp()

    def complete_current_task(self) -> Optional[str]:
        """Complete the current task and move to next in queue.

        Returns:
            Next task from queue if available, None otherwise
        """
        self.current_task = None

        if self.task_queue:
            next_task = self.task_queue.pop(0)
            self.set_current_task(next_task)
            return next_task
        else:
            self.status = ExecutionStatus.COMPLETED
            self.update_timestamp()
            return None

    def add_error(self, error_message: str) -> None:
        """Add an error message to the error log.

        Args:
            error_message: Error message to record
        """
        self.error_messages.append(f"{datetime.now().isoformat()}: {error_message}")
        self.status = ExecutionStatus.FAILED
        self.update_timestamp()

    def update_performance_metric(self, metric_name: str, value: float) -> None:
        """Update a performance metric.

        Args:
            metric_name: Name of the metric
            value: New value for the metric
        """
        self.performance_metrics[metric_name] = value
        self.update_timestamp()

    def update_resource_usage(self, resource_type: ResourceType, usage: float) -> None:
        """Update resource usage tracking.

        Args:
            resource_type: Type of resource being tracked
            usage: Current usage amount
        """
        self.resource_usage[resource_type.value] = usage
        self.update_timestamp()

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation history.

        Returns:
            Dictionary with conversation statistics
        """
        if not self.conversation_history:
            return {"total_messages": 0, "roles": []}

        roles = [msg["role"] for msg in self.conversation_history]
        return {
            "total_messages": len(self.conversation_history),
            "roles": list(set(roles)),
            "role_counts": {role: roles.count(role) for role in set(roles)},
            "latest_message": (
                self.conversation_history[-1] if self.conversation_history else None
            ),
        }

    def get_tool_usage_summary(self) -> Dict[str, Any]:
        """Get a summary of tool usage.

        Returns:
            Dictionary with tool usage statistics
        """
        if not self.tool_calls:
            return {"total_calls": 0, "tools_used": []}

        tools = [call["tool_name"] for call in self.tool_calls]
        return {
            "total_calls": len(self.tool_calls),
            "tools_used": list(set(tools)),
            "tool_counts": {tool: tools.count(tool) for tool in set(tools)},
            "latest_call": self.tool_calls[-1] if self.tool_calls else None,
        }


class WorkflowState(StateSchema):
    """State schema for workflow execution tracking.

    This schema manages the state of multi-step workflows, including step execution,
    dependencies, parallel processing, and error recovery.

    Attributes:
        workflow_name: Name of the workflow
        workflow_version: Version of the workflow definition
        steps: List of workflow steps with their states
        current_step_index: Index of currently executing step
        completed_steps: Set of completed step IDs
        failed_steps: Set of failed step IDs
        parallel_branches: Active parallel execution branches
        workflow_inputs: Initial inputs to the workflow
        workflow_outputs: Final outputs from the workflow
        step_dependencies: Dependencies between workflow steps

    Examples:
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
    """

    workflow_name: str = Field(..., description="Name of the workflow")
    workflow_version: str = Field(
        default="1.0.0", description="Version of the workflow definition"
    )
    steps: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of workflow steps with their states"
    )
    current_step_index: int = Field(
        default=-1, description="Index of currently executing step"
    )
    completed_steps: Set[str] = Field(
        default_factory=set, description="Set of completed step IDs"
    )
    failed_steps: Set[str] = Field(
        default_factory=set, description="Set of failed step IDs"
    )
    parallel_branches: Dict[str, List[str]] = Field(
        default_factory=dict, description="Active parallel execution branches"
    )
    workflow_inputs: Dict[str, Any] = Field(
        default_factory=dict, description="Initial inputs to the workflow"
    )
    workflow_outputs: Dict[str, Any] = Field(
        default_factory=dict, description="Final outputs from the workflow"
    )
    step_dependencies: Dict[str, List[str]] = Field(
        default_factory=dict, description="Dependencies between workflow steps"
    )

    def __init__(self, **kwargs):
        """Initialize workflow state with proper state type."""
        kwargs.setdefault("state_type", "workflow")
        super().__init__(**kwargs)

    def add_step(self, step_id: str, step_config: Dict[str, Any]) -> None:
        """Add a step to the workflow.

        Args:
            step_id: Unique identifier for the step
            step_config: Configuration for the step
        """
        step = {
            "step_id": step_id,
            "config": step_config,
            "status": ExecutionStatus.PENDING,
            "start_time": None,
            "end_time": None,
            "outputs": {},
            "error_message": None,
        }
        self.steps.append(step)
        self.update_timestamp()

    def add_step_dependency(self, step_id: str, depends_on: str) -> None:
        """Add a dependency relationship between steps.

        Args:
            step_id: ID of the step that has a dependency
            depends_on: ID of the step that must complete first
        """
        if step_id not in self.step_dependencies:
            self.step_dependencies[step_id] = []
        self.step_dependencies[step_id].append(depends_on)
        self.update_timestamp()

    def can_execute_step(self, step_id: str) -> bool:
        """Check if a step can be executed based on dependencies.

        Args:
            step_id: ID of the step to check

        Returns:
            True if step can be executed, False otherwise
        """
        dependencies = self.step_dependencies.get(step_id, [])
        return all(dep in self.completed_steps for dep in dependencies)

    def start_step(self, step_id: str) -> bool:
        """Start execution of a workflow step.

        Args:
            step_id: ID of the step to start

        Returns:
            True if step was started, False if dependencies not met
        """
        if not self.can_execute_step(step_id):
            return False

        # Find and update step
        for i, step in enumerate(self.steps):
            if step["step_id"] == step_id:
                step["status"] = ExecutionStatus.RUNNING
                step["start_time"] = datetime.now().isoformat()
                self.current_step_index = i
                break

        self.update_timestamp()
        return True

    def complete_step(self, step_id: str, outputs: Dict[str, Any]) -> None:
        """Mark a workflow step as completed.

        Args:
            step_id: ID of the completed step
            outputs: Outputs produced by the step
        """
        # Find and update step
        for step in self.steps:
            if step["step_id"] == step_id:
                step["status"] = ExecutionStatus.COMPLETED
                step["end_time"] = datetime.now().isoformat()
                step["outputs"] = outputs
                break

        self.completed_steps.add(step_id)
        self.update_timestamp()

    def fail_step(self, step_id: str, error_message: str) -> None:
        """Mark a workflow step as failed.

        Args:
            step_id: ID of the failed step
            error_message: Error message describing the failure
        """
        # Find and update step
        for step in self.steps:
            if step["step_id"] == step_id:
                step["status"] = ExecutionStatus.FAILED
                step["end_time"] = datetime.now().isoformat()
                step["error_message"] = error_message
                break

        self.failed_steps.add(step_id)
        self.update_timestamp()

    def get_executable_steps(self) -> List[str]:
        """Get list of steps that can currently be executed.

        Returns:
            List of step IDs that can be executed
        """
        executable = []
        for step in self.steps:
            step_id = step["step_id"]
            if (
                step["status"] == ExecutionStatus.PENDING
                and step_id not in self.failed_steps
                and self.can_execute_step(step_id)
            ):
                executable.append(step_id)
        return executable

    def get_workflow_progress(self) -> Dict[str, Any]:
        """Get overall workflow progress information.

        Returns:
            Dictionary with progress statistics
        """
        total_steps = len(self.steps)
        completed = len(self.completed_steps)
        failed = len(self.failed_steps)
        pending = total_steps - completed - failed

        return {
            "total_steps": total_steps,
            "completed_steps": completed,
            "failed_steps": failed,
            "pending_steps": pending,
            "progress_percentage": (
                (completed / total_steps * 100) if total_steps > 0 else 0
            ),
            "is_complete": pending == 0,
            "has_failures": failed > 0,
        }


class ExecutionContext(StateSchema):
    """Execution context schema for tracking runtime environments.

    This schema captures the complete execution environment including system resources,
    configuration parameters, environment variables, and runtime constraints.

    Attributes:
        context_name: Name of the execution context
        environment: Environment name (dev, staging, prod)
        system_info: System information and capabilities
        resource_limits: Resource usage limits
        environment_variables: Environment variable settings
        execution_parameters: Runtime execution parameters
        active_sessions: Currently active execution sessions
        monitoring_data: Performance and health monitoring data

    Examples:
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
    """

    context_name: str = Field(..., description="Name of the execution context")
    environment: str = Field(..., description="Environment name (dev, staging, prod)")
    system_info: Dict[str, Any] = Field(
        default_factory=dict, description="System information and capabilities"
    )
    resource_limits: Dict[str, float] = Field(
        default_factory=dict, description="Resource usage limits"
    )
    environment_variables: Dict[str, str] = Field(
        default_factory=dict, description="Environment variable settings"
    )
    execution_parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Runtime execution parameters"
    )
    active_sessions: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Currently active execution sessions"
    )
    monitoring_data: Dict[str, List[Tuple[datetime, float]]] = Field(
        default_factory=dict, description="Performance and health monitoring data"
    )

    def __init__(self, **kwargs):
        """Initialize execution context with proper state type."""
        kwargs.setdefault("state_type", "execution_context")
        super().__init__(**kwargs)

    def start_execution_session(
        self, session_name: str, parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start a new execution session.

        Args:
            session_name: Name/description of the session
            parameters: Optional session parameters

        Returns:
            Unique session ID
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        session = {
            "session_id": session_id,
            "session_name": session_name,
            "parameters": parameters or {},
            "status": ExecutionStatus.RUNNING,
            "start_time": datetime.now(),
            "end_time": None,
            "outputs": {},
            "resource_usage": {},
        }
        self.active_sessions[session_id] = session
        self.update_timestamp()
        return session_id

    def update_session_status(self, session_id: str, status: ExecutionStatus) -> None:
        """Update the status of an execution session.

        Args:
            session_id: ID of the session to update
            status: New status for the session
        """
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["status"] = status
            self.update_timestamp()

    def end_execution_session(
        self, session_id: str, outputs: Optional[Dict[str, Any]] = None
    ) -> None:
        """End an execution session.

        Args:
            session_id: ID of the session to end
            outputs: Optional session outputs
        """
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session["status"] = ExecutionStatus.COMPLETED
            session["end_time"] = datetime.now()
            session["outputs"] = outputs or {}
            self.update_timestamp()

    def update_monitoring_data(self, metric_name: str, value: float) -> None:
        """Update monitoring data with a new metric value.

        Args:
            metric_name: Name of the metric
            value: New metric value
        """
        if metric_name not in self.monitoring_data:
            self.monitoring_data[metric_name] = []

        self.monitoring_data[metric_name].append((datetime.now(), value))

        # Keep only last 1000 data points
        if len(self.monitoring_data[metric_name]) > 1000:
            self.monitoring_data[metric_name] = self.monitoring_data[metric_name][
                -1000:
            ]

        self.update_timestamp()

    def check_resource_limits(self) -> Dict[str, bool]:
        """Check if current resource usage is within limits.

        Returns:
            Dictionary showing which limits are exceeded
        """
        violations = {}

        for resource, limit in self.resource_limits.items():
            if resource in self.monitoring_data:
                # Get latest value
                latest_data = self.monitoring_data[resource]
                if latest_data:
                    current_usage = latest_data[-1][1]
                    violations[resource] = current_usage > limit
                else:
                    violations[resource] = False
            else:
                violations[resource] = False

        return violations

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of execution sessions.

        Returns:
            Dictionary with session statistics
        """
        if not self.active_sessions:
            return {"total_sessions": 0, "active_sessions": 0}

        statuses = [session["status"] for session in self.active_sessions.values()]
        active_count = sum(
            1 for status in statuses if status == ExecutionStatus.RUNNING
        )

        return {
            "total_sessions": len(self.active_sessions),
            "active_sessions": active_count,
            "completed_sessions": statuses.count(ExecutionStatus.COMPLETED),
            "failed_sessions": statuses.count(ExecutionStatus.FAILED),
            "status_distribution": {
                status.value: statuses.count(status) for status in ExecutionStatus
            },
        }
