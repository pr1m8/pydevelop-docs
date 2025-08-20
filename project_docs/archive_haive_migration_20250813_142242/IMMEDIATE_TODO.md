# PyDevelop-Docs Immediate TODO List

**Created**: 2025-01-13  
**Priority**: High  
**Target**: Next 2 weeks

## 🚀 Phase 1: Quick Wins (Start Immediately)

### Week 1: Foundation Setup

#### Day 1-2: Hub Enhancements

- [ ] **Add user journey navigation to hub**
  - [ ] Create "For New Users" section in hub index
  - [ ] Add "For Developers" section with architecture links
  - [ ] Add "For Contributors" section with development guides
  - [ ] Update hub CSS for better section styling

- [ ] **Enhance package descriptions**
  - [ ] Update `_get_package_description()` in `link_builder.py`
  - [ ] Add difficulty levels (🟢 Beginner, 🟡 Intermediate, 🔴 Advanced)
  - [ ] Add estimated learning time for each package
  - [ ] Add "Most Popular" badges based on page count

#### Day 3-4: Cross-Package Content

- [ ] **Create first cross-package tutorial**
  - [ ] "Build a Simple Research Assistant" tutorial
  - [ ] Uses haive-core + haive-agents + haive-tools
  - [ ] Add to `docs/source/tutorials/` directory
  - [ ] Link from hub main page

- [ ] **Create package selection guide**
  - [ ] "Choose the Right Package" decision matrix
  - [ ] Interactive flowchart: Use case → Recommended packages
  - [ ] Add to hub navigation

#### Day 5: GitHub Actions Setup

- [ ] **Create basic documentation CI/CD**
  - [ ] `.github/workflows/docs.yml` with basic pipeline
  - [ ] Trigger on docs changes in packages/
  - [ ] Build hub automatically on main branch
  - [ ] Deploy to GitHub Pages

### Week 2: Interactive Features

#### Day 6-8: Search Enhancement

- [ ] **Implement unified search**
  - [ ] Add search filters to hub (Examples, API, Guides)
  - [ ] Create search results page with package categorization
  - [ ] Add search suggestions based on popular queries
  - [ ] Test search across all 6 packages

#### Day 9-10: Package Templates

- [ ] **Create enhanced package structure template**
  - [ ] `quickstart/index.rst` template for each package
  - [ ] `examples/` directory with sample files
  - [ ] `guides/` directory with tutorial templates
  - [ ] Apply to haive-core as pilot package

## 🛠️ Scripts to Create This Week

### Priority 1: Essential Scripts

- [ ] **`scripts/enhance-hub-navigation.py`**

  ```python
  """Add enhanced navigation sections to documentation hub."""
  def create_user_journey_sections():
      # Create For New Users, Developers, Contributors sections
      pass

  def add_package_difficulty_badges():
      # Add difficulty and time estimates
      pass
  ```

- [ ] **`scripts/create-cross-package-tutorial.py`**
  ```python
  """Generate cross-package tutorial templates."""
  def create_research_assistant_tutorial():
      # Template for multi-package workflow
      pass
  ```

### Priority 2: Automation Scripts

- [ ] **`scripts/detect-doc-changes.py`**

  ```python
  """Smart detection of which packages need documentation rebuilds."""
  import subprocess
  import json

  def detect_changed_packages():
      # Git-based change detection
      # Return JSON array of changed packages
      pass
  ```

- [ ] **`scripts/setup-github-actions.py`**
  ```python
  """Generate GitHub Actions workflow for documentation CI/CD."""
  def create_docs_workflow():
      # Generate .github/workflows/docs.yml
      pass
  ```

## 🎯 Specific File Changes

### 1. Update Link Builder (`link_builder.py`)

```python
# Enhance package descriptions with difficulty and time
def _get_package_description(self, name: str) -> str:
    descriptions = {
        "haive-core": "🟡 Core framework and infrastructure (Est. 30 min)",
        "haive-agents": "🟢 Pre-built agent implementations (Est. 15 min)",
        "haive-tools": "🟢 Tool integrations and utilities (Est. 20 min)",
        "haive-games": "🔴 Game environments and AI strategies (Est. 45 min)",
        "haive-mcp": "🟡 Model Context Protocol integration (Est. 25 min)",
        "haive-dataflow": "🔴 Streaming and data processing (Est. 60 min)",
    }
    return descriptions.get(name, f"Documentation for {name}")
```

### 2. Create Hub Navigation Template

```restructuredtext
# Add to hub index.rst
Quick Start by Experience Level
===============================

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 🚀 New to Haive?
      :link: quickstart/index
      :shadow: md

      **Start here** - 5-minute introduction to building your first agent

      *Estimated time: 5 minutes*

   .. grid-item-card:: 👩‍💻 I'm a Developer
      :link: developers/index
      :shadow: md

      **Architecture overview** - Deep dive into framework components

      *Estimated time: 30 minutes*

   .. grid-item-card:: 🤝 I Want to Contribute
      :link: contributors/index
      :shadow: md

      **Contribution guide** - How to extend and improve Haive

      *Estimated time: 20 minutes*
```

### 3. Create First Cross-Package Tutorial

File: `docs/source/tutorials/research-assistant.rst`

```restructuredtext
Build a Research Assistant in 15 Minutes
=========================================

This tutorial shows how to combine multiple Haive packages to create
a research assistant that can search the web and provide structured answers.

**Packages used:**
- :doc:`haive-core <haive-core:index>` - Configuration and state management
- :doc:`haive-agents <haive-agents:index>` - ReactAgent for reasoning
- :doc:`haive-tools <haive-tools:index>` - Web search integration

**Prerequisites:** Basic Python knowledge, 15 minutes

Step 1: Core Setup (:doc:`haive-core <haive-core:quickstart>`)
-------------------------------------------------------------

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMConfig

   # Configure the LLM engine
   config = AugLLMConfig(
       temperature=0.7,
       max_tokens=1000
   )

Step 2: Add Web Search (:doc:`haive-tools <haive-tools:integrations/web-search>`)
-------------------------------------------------------------------------------

.. code-block:: python

   from haive.tools.web_search import WebSearchTool

   # Add web search capability
   search_tool = WebSearchTool()

Step 3: Create Research Agent (:doc:`haive-agents <haive-agents:react-agent>`)
-----------------------------------------------------------------------------

.. code-block:: python

   from haive.agents.react import ReactAgent

   # Combine everything into a research agent
   research_agent = ReactAgent(
       name="research_assistant",
       engine=config,
       tools=[search_tool]
   )

   # Use the agent
   result = research_agent.run("What are the latest developments in AI safety?")
   print(result)

🎉 **Congratulations!** You've built a research assistant that can search the web and provide intelligent answers.

**Next Steps:**
- :doc:`Add memory <haive-core:guides/memory>` to remember past conversations
- :doc:`Structure output <haive-agents:guides/structured-output>` for consistent formatting
- :doc:`Deploy your agent <haive-prebuilt:deployment>` for production use
```

## ✅ Success Criteria for Week 1-2

### Week 1 Complete When:

- [ ] Hub has clear user journey navigation (New Users/Developers/Contributors)
- [ ] All 6 packages have enhanced descriptions with difficulty/time
- [ ] First cross-package tutorial is live and accessible from hub
- [ ] Basic GitHub Actions pipeline is operational

### Week 2 Complete When:

- [ ] Search works across all packages with filters
- [ ] Package selection guide helps users choose right components
- [ ] At least 1 package (haive-core) has enhanced structure template
- [ ] Documentation automatically rebuilds on changes

## 🚨 Blockers to Watch For

1. **GitHub Actions permissions** - May need repository settings changes
2. **Search indexing** - Sphinx search might need configuration
3. **Cross-package linking** - Intersphinx paths might break
4. **Build performance** - Large documentation set may cause timeouts

## 📞 Daily Check-ins

- **Day 1**: Hub navigation enhancement complete?
- **Day 3**: Cross-package tutorial accessible?
- **Day 5**: GitHub Actions pipeline working?
- **Day 8**: Search functionality operational?
- **Day 10**: Package templates ready for rollout?

---

**Ready to start?** Begin with enhancing the hub navigation - it's the highest impact, lowest effort improvement that users will see immediately.
