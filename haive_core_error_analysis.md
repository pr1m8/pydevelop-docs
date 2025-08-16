# Haive-Core Documentation Build Error Analysis

## Summary

- **Total Critical Errors**: 65
- **Root Cause**: AutoAPI is trying to import class names from docstring examples as if they were real modules

## Error Pattern

All 65 errors follow this pattern:

```
ModuleNotFoundError: No module named 'ClassName'
```

These are NOT real import errors in the code. They occur because:

1. Docstrings contain example code like:

   ```python
   Examples:
       Basic usage::

           from haive.core.models.llm.providers.ai21 import AI21Provider
   ```

2. AutoAPI parses these docstring examples and tries to validate the imports

3. It incorrectly tries to import `AI21Provider` as a module, when it's actually a class

## Affected Modules by Category

### Provider Classes (19 errors)

- AI21Provider, AnthropicProvider, AzureOpenAIProvider, BedrockProvider
- CohereProvider, FireworksProvider, GeminiProvider, GroqProvider
- HuggingFaceProvider, MistralProvider, NVIDIAProvider, OllamaProvider
- OpenAIProvider, ReplicateProvider, TogetherProvider, VertexAIProvider, XAIProvider
- BaseLLMProvider, EmbeddingProvider

### Configuration Classes (8 errors)

- LLMConfig, EngineNodeConfig, OpenAIEmbeddingConfig, RetrieverConfig
- VectorStoreConfig, VectorStoreRetrieverConfig, ValidationNodeConfig
- GithubSettings, GithubRepo

### Factory/Utility Functions (8 errors)

- LLMFactory, LLMProvider, NodeFactory, NodeRegistry
- create_llm, create_node, create_engine_node
- get_available_providers, get_provider_models

### Other Classes (30 errors)

- Agent, AgentNodeV3, Field, FieldMapping
- FilterBuilder, FilterCriteria, MetadataMixin, ModelMetadata
- NodeSchemaComposer, ProviderImportError, RetrieverType
- RoutingValidationNode, UnifiedValidationNode, Validation
- VectorStoreProvider (appears twice)
- Various others

## Solution Options

1. **Modify docstrings** to use different example format that AutoAPI won't parse
2. **Configure AutoAPI** to skip parsing docstring examples
3. **Add mock imports** for documentation build only
4. **Use autodoc** instead of AutoAPI for problematic modules

## Impact

Despite these 65 critical errors, they only affect the documentation build, not the actual code functionality. The packages that import haive-core should still build successfully.
