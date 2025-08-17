# Union Type Error Research Plan - PyDevelop-Docs & Haive Framework

**Created**: 2025-08-15
**Status**: Active Research
**Issue**: TypeError with union type operator (`|`) causing critical documentation build failures

## 🎯 Executive Summary

Critical documentation build failures in haive-core and haive-agents due to Python 3.10+ union type syntax (`str | None`) conflicting with sphinx_codeautolink extension parsing. This affects 2 out of 7 packages with cascading failures.

## 🔴 Critical Error Details

### Error Signature

```
TypeError: unsupported operand type(s) for |: 'str' and 'NoneType'
```

### Affected Packages

1. **haive-core**: 4 critical errors, build completely failed
2. **haive-agents**: 3 critical errors, build completely failed
3. **haive-tools**: Build succeeded (no union type issues)
4. **Other packages**: Unknown status due to build interruption

### Error Context

```
Extension 'sphinx_codeautolink.extension' failed
Handler <bound method SphinxCodeAutoLink.parse_blocks> for event 'doctree-read' threw an exception
Document: 'autoapi/haive/core/engine/agent/agent/index'
```

## 📍 Research Plan

### Phase 1: Error Localization (Immediate)

#### 1.1 Identify Exact Source Files

```bash
# Find all Python files with union type syntax
find /home/will/Projects/haive/backend/haive/packages/haive-core -name "*.py" -exec grep -l "|\s*None" {} \; | head -20

# Find specifically in agent.py files
find /home/will/Projects/haive/backend/haive/packages/haive-core -path "*/engine/agent/agent.py" -exec grep -n "|\s*None" {} \;

# Search for all union type annotations
rg --type py "\w+\s*\|\s*\w+" /home/will/Projects/haive/backend/haive/packages/haive-core/src
```

#### 1.2 Analyze AutoAPI Generated Files

```bash
# Check the specific failing document
cat /home/will/Projects/haive/backend/haive/packages/haive-core/docs/build/autoapi/haive/core/engine/agent/agent/index.rst

# Look for union types in generated RST
grep -r "|\s*None" /home/will/Projects/haive/backend/haive/packages/haive-core/docs/build/autoapi/
```

#### 1.3 Extension Interaction Analysis

```bash
# Check sphinx_codeautolink version
poetry show sphinx-codeautolink

# Find where codeautolink processes type annotations
grep -n "parse_blocks" $(poetry run python -c "import sphinx_codeautolink; print(sphinx_codeautolink.__file__)")
```

### Phase 2: Root Cause Analysis

#### 2.1 Type Annotation Patterns

- **Modern Union Syntax**: `str | None`, `int | float`, `List[str] | None`
- **Legacy Union Syntax**: `Union[str, None]`, `Optional[str]`
- **Complex Unions**: `str | int | None`, `Dict[str, Any] | List[Any] | None`

#### 2.2 Where Union Types Occur

1. **Function Return Types**

   ```python
   def get_agent() -> Agent | None:
   ```

2. **Parameter Types**

   ```python
   def process(data: str | bytes | None = None):
   ```

3. **Class Attributes**

   ```python
   class AgentConfig:
       name: str | None
       tools: List[str] | None
   ```

4. **Type Aliases**
   ```python
   ConfigType = Dict[str, Any] | str | None
   ```

#### 2.3 Extension Processing Flow

1. AutoAPI reads Python files and extracts type annotations
2. sphinx_codeautolink parses these to create cross-references
3. Union operator `|` causes type evaluation where one side is None
4. Extension tries to perform operation on string and NoneType

### Phase 3: Solution Investigation

#### 3.1 Quick Fixes (Temporary)

1. **Disable sphinx_codeautolink**

   ```python
   # In config.py, comment out:
   # "sphinx_codeautolink",
   ```

2. **Downgrade to typing.Union**

   ```python
   # Replace: str | None
   # With: Union[str, None] or Optional[str]
   ```

3. **Configure extension to skip union types**
   ```python
   codeautolink_skip_blocks = ["str | None", "| None"]
   ```

#### 3.2 Proper Fixes (Permanent)

1. **Update sphinx_codeautolink** to support PEP 604 union syntax
2. **Use `from __future__ import annotations`** to defer evaluation
3. **Configure AutoAPI to handle modern syntax**
4. **Create custom type annotation parser**

### Phase 4: Testing Strategy

#### 4.1 Create Test Case

```python
# test_union_types.py
from typing import Union, Optional

class ModernAgent:
    """Agent with modern type hints."""

    def process(self, data: str | None) -> dict | None:
        """Process data with union return type."""
        return {"result": data} if data else None

    async def async_process(self, config: dict | list | None = None) -> str | int:
        """Async method with complex union."""
        return "success"

class LegacyAgent:
    """Agent with legacy type hints."""

    def process(self, data: Optional[str]) -> Optional[dict]:
        """Process data with Optional return type."""
        return {"result": data} if data else None
```

#### 4.2 Build Testing

```bash
# Test single file documentation
echo "Testing union type handling..."
cd test-projects/union-type-test
poetry run pydevelop-docs init
poetry run pydevelop-docs build

# Check for errors
grep -i "unsupported operand" docs/build/build.log
```

### Phase 5: Implementation Plan

#### 5.1 Immediate Actions

1. **Document all union type occurrences** in affected packages
2. **Test with sphinx_codeautolink disabled**
3. **Create migration script** for union type syntax if needed

#### 5.2 Short-term Solutions

1. **Version compatibility matrix** for extensions
2. **Configuration tweaks** for AutoAPI/codeautolink
3. **Selective disabling** for problematic files

#### 5.3 Long-term Solutions

1. **Extension updates** or replacements
2. **Custom preprocessing** for modern syntax
3. **Contributing fixes** upstream to sphinx_codeautolink

## 📊 Impact Analysis

### Affected Systems

- **Documentation Generation**: 2/7 packages failing completely
- **CI/CD Pipeline**: Documentation builds will fail
- **Developer Experience**: Cannot generate docs for core packages
- **API Reference**: Missing critical package documentation

### Risk Assessment

- **High**: Core packages (haive-core, haive-agents) are undocumented
- **Medium**: Other packages may have hidden union type issues
- **Low**: haive-tools confirmed working (no union types?)

## 🔍 Investigation Commands

```bash
# 1. Find all union type patterns
find /home/will/Projects/haive/backend/haive/packages -name "*.py" -exec grep -l "|\s*None\||\s*\w\+" {} \; | sort | uniq

# 2. Count union type occurrences per package
for pkg in haive-core haive-agents haive-tools; do
    echo "=== $pkg ==="
    find /home/will/Projects/haive/backend/haive/packages/$pkg -name "*.py" -exec grep -c "|\s*None\||\s*\w\+" {} \; | paste -sd+ | bc
done

# 3. Extract problematic type annotations
rg --type py "def.*\).*->.*\|.*:" -A 2 /home/will/Projects/haive/backend/haive/packages/haive-core/src

# 4. Check Python version compatibility
python --version
poetry run python -c "import sys; print(f'Python {sys.version}')"

# 5. Analyze sphinx_codeautolink source
poetry run python -c "import sphinx_codeautolink; import inspect; print(inspect.getsourcefile(sphinx_codeautolink))"
```

## 📈 Success Metrics

1. **All packages build successfully** without TypeError
2. **Union type syntax preserved** in source code
3. **Cross-references work** for modern type annotations
4. **No regression** in documentation quality
5. **Build time remains reasonable** (<5 min per package)

## 🚨 Fallback Strategy

If union type syntax cannot be supported:

1. **Create pre-processor script** to convert union types before build
2. **Use type: ignore comments** for problematic annotations
3. **Generate documentation without cross-references** (disable codeautolink)
4. **Document known limitations** in build guide

## 📝 Next Steps

1. **Execute Phase 1.1** - Locate exact files with union types
2. **Run test build** with sphinx_codeautolink disabled
3. **Document findings** in implementation report
4. **Create fix PR** based on chosen solution

---

**Related Issues**:

- [Python 3.10 Union Types (PEP 604)](https://www.python.org/dev/peps/pep-0604/)
- [sphinx_codeautolink GitHub Issues](https://github.com/felix-hilden/sphinx-codeautolink/issues)
- Build logs: `/home/will/Projects/haive/backend/haive/tools/pydevelop-docs/build_output.log`
