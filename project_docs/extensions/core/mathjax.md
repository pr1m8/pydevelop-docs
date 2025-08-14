# sphinx.ext.mathjax - Mathematical Notation Support

**Extension**: `sphinx.ext.mathjax`  
**Priority**: Core Foundation (Position 7 in extensions list)  
**Official Documentation**: [sphinx.ext.mathjax](https://www.sphinx-doc.org/en/master/usage/extensions/mathjax.html)  
**Status in PyDevelop-Docs**: ✅ Implemented for mathematical documentation

## Overview

`sphinx.ext.mathjax` enables beautiful mathematical notation in Sphinx documentation using MathJax, a JavaScript library for rendering mathematical formulas. This extension is essential for documenting algorithms, statistical models, mathematical functions, and any content requiring mathematical expressions, making it particularly valuable for AI/ML and scientific computing documentation.

## Core Capabilities

### 1. Mathematical Notation Rendering

- **LaTeX Support**: Full LaTeX mathematical notation syntax
- **Inline Math**: Mathematical expressions within text paragraphs
- **Display Math**: Centered mathematical equations and formulas
- **Complex Expressions**: Support for matrices, integrals, summations, and advanced notation

### 2. Cross-Platform Compatibility

- **Web Rendering**: Client-side JavaScript rendering in browsers
- **Mobile Support**: Responsive mathematical notation on all devices
- **Accessibility**: Screen reader compatible mathematical content
- **Print Support**: High-quality mathematical notation in print formats

### 3. Integration Features

- **Equation Numbering**: Automatic numbering and referencing of equations
- **Cross-References**: Link to equations from other parts of documentation
- **Custom Macros**: Define reusable mathematical expressions
- **Theme Integration**: Mathematical notation matches documentation theme

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - mathjax extension included in core
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",  # Mathematical notation support
    # ... other extensions
]

# Basic mathjax configuration (uses defaults)
# Standard MathJax 3.x configuration enabled
```

### Enhanced Configuration Options

```python
# Advanced MathJax configuration for PyDevelop-Docs
mathjax3_config = {
    'tex': {
        'inlineMath': [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
        'processEscapes': True,
        'processEnvironments': True,
        'tags': 'ams',  # AMS equation numbering
        'macros': {
            # Common AI/ML notation macros
            'RR': r'\mathbb{R}',
            'NN': r'\mathbb{N}',
            'ZZ': r'\mathbb{Z}',
            'QQ': r'\mathbb{Q}',
            'CC': r'\mathbb{C}',
            'argmax': r'\operatorname*{argmax}',
            'argmin': r'\operatorname*{argmin}',
            'softmax': r'\operatorname{softmax}',
            'relu': r'\operatorname{ReLU}',
            'sigmoid': r'\sigma',
            'tanh': r'\operatorname{tanh}',
            'loss': r'\mathcal{L}',
            'prob': r'\mathbb{P}',
            'expect': r'\mathbb{E}',
            'var': r'\operatorname{Var}',
            'cov': r'\operatorname{Cov}',
            'normal': r'\mathcal{N}',
            'uniform': r'\operatorname{Uniform}',
            'kl': r'\operatorname{KL}',
            'entropy': r'\operatorname{H}',
            'transpose': r'^{\top}',
            'inverse': r'^{-1}',
            'pinverse': r'^{\dagger}',
        },
        'environments': {
            'algorithm': ['\\begin{algorithm}', '\\end{algorithm}'],
            'proof': ['\\begin{proof}', '\\end{proof}'],
        }
    },
    'svg': {
        'fontCache': 'global',
        'scale': 1.0,
        'minScale': 0.5,
        'mtextInheritFont': True,
        'merrorInheritFont': True,
        'mathvariantInheritFont': True,
        'fontURL': 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/svg/fonts/tex-svg'
    },
    'chtml': {
        'scale': 1.0,
        'minScale': 0.5,
        'mtextInheritFont': True,
        'merrorInheritFont': True
    },
    'options': {
        'enableMenu': True,
        'menuOptions': {
            'settings': {
                'zoom': 'Click',
                'zscale': '150%'
            }
        }
    },
    'loader': {
        'load': ['input/tex', 'output/svg', 'ui/menu'],
        'paths': {'mathjax': 'https://cdn.jsdelivr.net/npm/mathjax@3/es5'}
    }
}

# Alternative: Use local MathJax for offline documentation
mathjax_path = "mathjax/tex-svg.js"  # For offline builds

# Equation numbering and references
math_number_all = True  # Number all display equations
math_eqref_format = "Eq. {number}"
math_numfig = True  # Enable figure numbering
```

### AI/ML Specific Configuration

```python
# Enhanced configuration for AI/ML documentation
mathjax3_config['tex']['packages'] = {
    '[+]': ['ams', 'amsmath', 'amssymb', 'cases', 'color', 'mathtools']
}

# Additional AI/ML macros
mathjax3_config['tex']['macros'].update({
    # Neural networks
    'neuron': r'\mathbf{n}',
    'layer': r'\mathbf{l}',
    'weight': r'\mathbf{W}',
    'bias': r'\mathbf{b}',
    'activation': r'\phi',
    'gradient': r'\nabla',
    'backprop': r'\frac{\partial \loss}{\partial \theta}',

    # Machine learning
    'dataset': r'\mathcal{D}',
    'model': r'\mathcal{M}',
    'params': r'\theta',
    'features': r'\mathbf{x}',
    'labels': r'\mathbf{y}',
    'predictions': r'\hat{\mathbf{y}}',
    'accuracy': r'\text{Acc}',
    'precision': r'\text{Prec}',
    'recall': r'\text{Rec}',
    'f1': r'\text{F}_1',

    # Probability and statistics
    'gaussian': r'\mathcal{N}(\mu, \sigma^2)',
    'bernoulli': r'\text{Bern}(p)',
    'categorical': r'\text{Cat}(\mathbf{p})',
    'likelihood': r'\mathcal{L}(\theta | \dataset)',
    'posterior': r'p(\theta | \dataset)',
    'prior': r'p(\theta)',

    # Optimization
    'minimize': r'\min_{\theta}',
    'maximize': r'\max_{\theta}',
    'subject': r'\text{s.t.}',
    'learningrate': r'\alpha',
    'momentum': r'\beta',
    'regularization': r'\lambda',
})
```

## Template Integration Opportunities

### 1. Mathematical API Documentation

```jinja2
{# _autoapi_templates/python/function.rst #}
{% if obj.has_mathematical_content %}
.. py:function:: {{ obj.id }}{{ obj.args }}

   {% if obj.docstring %}
   {{ obj.docstring|prepare_docstring|process_math|indent(3) }}
   {% endif %}

   {% if obj.mathematical_description %}
   **Mathematical Description:**

   {{ obj.mathematical_description|process_math }}
   {% endif %}

   {% if obj.algorithm_complexity %}
   **Complexity:**

   * Time: :math:`{{ obj.algorithm_complexity.time }}`
   * Space: :math:`{{ obj.algorithm_complexity.space }}`
   {% endif %}

   {% if obj.mathematical_examples %}
   **Mathematical Examples:**

   {% for example in obj.mathematical_examples %}
   {{ example.description }}

   .. math::
      {{ example.equation }}

   {% endfor %}
   {% endif %}
{% endif %}
```

### 2. Algorithm Documentation Templates

```jinja2
{# Enhanced algorithm documentation with mathematical notation #}
{% macro render_algorithm_with_math(obj) %}
{% if obj.algorithm_definition %}
.. admonition:: Algorithm Definition
   :class: algorithm-definition

   **{{ obj.algorithm_name }}**

   {% if obj.algorithm_input %}
   **Input:** {{ obj.algorithm_input|process_math }}
   {% endif %}

   {% if obj.algorithm_output %}
   **Output:** {{ obj.algorithm_output|process_math }}
   {% endif %}

   {% if obj.algorithm_steps %}
   **Steps:**

   {% for step in obj.algorithm_steps %}
   {{ loop.index }}. {{ step|process_math }}
   {% endfor %}
   {% endif %}

   {% if obj.algorithm_formula %}
   **Core Formula:**

   .. math::
      {{ obj.algorithm_formula }}
   {% endif %}

   {% if obj.algorithm_complexity %}
   **Complexity Analysis:**

   * Time Complexity: :math:`{{ obj.algorithm_complexity.time }}`
   * Space Complexity: :math:`{{ obj.algorithm_complexity.space }}`
   * Best Case: :math:`{{ obj.algorithm_complexity.best_case }}`
   * Worst Case: :math:`{{ obj.algorithm_complexity.worst_case }}`
   {% endif %}
{% endif %}
{% endmacro %}
```

### 3. Mathematical Class Documentation

```jinja2
{# Mathematical model class documentation #}
{% if obj.is_mathematical_model %}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|process_math|indent(0) }}
{% endif %}

{% if obj.mathematical_foundation %}
Mathematical Foundation
----------------------

{{ obj.mathematical_foundation|process_math }}
{% endif %}

{% if obj.equations %}
Key Equations
------------

{% for equation in obj.equations %}
.. math::
   :label: {{ equation.label }}

   {{ equation.formula }}

{{ equation.description|process_math }}

{% endfor %}
{% endif %}

{% if obj.mathematical_properties %}
Mathematical Properties
----------------------

{% for property in obj.mathematical_properties %}
**{{ property.name }}:**

{% if property.equation %}
.. math::
   {{ property.equation }}
{% endif %}

{{ property.description|process_math }}

{% endfor %}
{% endif %}
{% endif %}
```

## Best Practices for PyDevelop-Docs

### 1. Mathematical Algorithm Documentation

```python
class GradientDescentOptimizer:
    """Gradient descent optimization algorithm.

    This implementation uses the standard gradient descent update rule
    to minimize a loss function :math:`\\loss(\\theta)`.

    The algorithm iteratively updates parameters according to:

    .. math::
        \\theta_{t+1} = \\theta_t - \\learningrate \\nabla \\loss(\\theta_t)

    where :math:`\\learningrate` is the learning rate and
    :math:`\\nabla \\loss(\\theta_t)` is the gradient of the loss function
    at iteration :math:`t`.

    Args:
        learning_rate: Step size :math:`\\learningrate` for parameter updates.
            Typical range: :math:`[10^{-4}, 10^{-1}]`.
        momentum: Momentum coefficient :math:`\\momentum` for acceleration.
            Set to 0 for standard gradient descent.

    Example:
        Basic optimization setup:

        >>> optimizer = GradientDescentOptimizer(learning_rate=0.01)
        >>> for epoch in range(100):
        ...     loss = model.forward(data)
        ...     gradients = model.backward(loss)
        ...     optimizer.step(gradients)

        With momentum:

        >>> optimizer = GradientDescentOptimizer(
        ...     learning_rate=0.01,
        ...     momentum=0.9
        ... )

    Note:
        The convergence rate of gradient descent depends on the condition
        number :math:`\\kappa` of the Hessian matrix. For well-conditioned
        problems, the convergence rate is :math:`O(\\log(1/\\epsilon))`.

    Mathematical Properties:
        * **Convergence Rate**: :math:`O(1/k)` for convex functions
        * **Memory Complexity**: :math:`O(|\\params|)` where :math:`|\\params|`
          is the number of parameters
        * **Per-iteration Cost**: :math:`O(|\\dataset|)` for full batch gradient
    """

    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.0):
        """Initialize gradient descent optimizer."""
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.velocity = None

    def step(self, gradients: Dict[str, float]) -> None:
        """Perform single optimization step.

        Updates parameters using the gradient descent rule with optional momentum:

        .. math::
            \\begin{align}
            v_{t+1} &= \\momentum \\cdot v_t + \\nabla \\loss(\\theta_t) \\\\
            \\theta_{t+1} &= \\theta_t - \\learningrate \\cdot v_{t+1}
            \\end{align}

        Args:
            gradients: Dictionary of parameter gradients
                :math:`\\nabla \\loss(\\theta_t)`.

        Note:
            When :math:`\\momentum = 0`, this reduces to standard gradient descent:
            :math:`\\theta_{t+1} = \\theta_t - \\learningrate \\nabla \\loss(\\theta_t)`.
        """
        if self.velocity is None:
            self.velocity = {key: 0.0 for key in gradients.keys()}

        for param_name, grad in gradients.items():
            # Momentum update
            self.velocity[param_name] = (
                self.momentum * self.velocity[param_name] + grad
            )

            # Parameter update
            # Implementation implements the mathematical formula above
            pass
```

### 2. Statistical Model Documentation

```python
class NormalDistribution:
    """Normal (Gaussian) distribution implementation.

    The normal distribution is characterized by its probability density function:

    .. math::
        f(x | \\mu, \\sigma^2) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}}
        \\exp\\left(-\\frac{(x-\\mu)^2}{2\\sigma^2}\\right)

    where :math:`\\mu` is the mean and :math:`\\sigma^2` is the variance.

    Key Properties:
        * **Mean**: :math:`\\expect[X] = \\mu`
        * **Variance**: :math:`\\var[X] = \\sigma^2`
        * **Standard Deviation**: :math:`\\sigma`
        * **Entropy**: :math:`\\entropy(X) = \\frac{1}{2}\\log(2\\pi e \\sigma^2)`
        * **KL Divergence**: For two normal distributions
          :math:`\\normal(\\mu_1, \\sigma_1^2)` and :math:`\\normal(\\mu_2, \\sigma_2^2)`:

          .. math::
              \\kl(N_1 \\| N_2) = \\log\\frac{\\sigma_2}{\\sigma_1} +
              \\frac{\\sigma_1^2 + (\\mu_1 - \\mu_2)^2}{2\\sigma_2^2} - \\frac{1}{2}

    Args:
        mean: Distribution mean :math:`\\mu`.
        variance: Distribution variance :math:`\\sigma^2 > 0`.

    Example:
        Create and sample from normal distribution:

        >>> dist = NormalDistribution(mean=0.0, variance=1.0)
        >>> samples = dist.sample(1000)
        >>> abs(samples.mean() - 0.0) < 0.1  # Should be close to 0
        True

        Calculate probability density:

        >>> dist.pdf(0.0)  # PDF at mean
        0.39894228040143265
        >>> dist.pdf(1.0)  # PDF at one standard deviation
        0.24197072451914337

    Mathematical Relationships:
        The normal distribution is related to other distributions:

        * **Chi-squared**: If :math:`X \\sim \\normal(0, 1)`, then
          :math:`X^2 \\sim \\chi^2(1)`
        * **Log-normal**: If :math:`X \\sim \\normal(\\mu, \\sigma^2)`, then
          :math:`e^X \\sim \\text{LogNormal}(\\mu, \\sigma^2)`
        * **Central Limit Theorem**: Sample means converge to normal distribution
    """

    def __init__(self, mean: float = 0.0, variance: float = 1.0):
        """Initialize normal distribution parameters."""
        if variance <= 0:
            raise ValueError("Variance must be positive")
        self.mean = mean
        self.variance = variance
        self.std = math.sqrt(variance)

    def pdf(self, x: float) -> float:
        """Calculate probability density function.

        Evaluates the PDF at point :math:`x`:

        .. math::
            f(x) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}}
            \\exp\\left(-\\frac{(x-\\mu)^2}{2\\sigma^2}\\right)

        Args:
            x: Point at which to evaluate PDF.

        Returns:
            float: Probability density at :math:`x`.

        Example:
            >>> dist = NormalDistribution(0, 1)
            >>> dist.pdf(0)  # Maximum at mean
            0.39894228040143265
        """
        coefficient = 1.0 / math.sqrt(2 * math.pi * self.variance)
        exponent = -((x - self.mean) ** 2) / (2 * self.variance)
        return coefficient * math.exp(exponent)
```

### 3. Neural Network Mathematical Documentation

```python
class MultiLayerPerceptron:
    """Multi-layer perceptron neural network.

    This implementation uses standard feedforward architecture with
    configurable activation functions and layer sizes.

    Forward Pass:
        For layer :math:`l` with input :math:`\\mathbf{x}^{(l-1)}`:

        .. math::
            \\begin{align}
            \\mathbf{z}^{(l)} &= \\weight^{(l)} \\mathbf{x}^{(l-1)} + \\bias^{(l)} \\\\
            \\mathbf{x}^{(l)} &= \\activation(\\mathbf{z}^{(l)})
            \\end{align}

    Backpropagation:
        Error gradients are computed using the chain rule:

        .. math::
            \\begin{align}
            \\frac{\\partial \\loss}{\\partial \\weight^{(l)}} &=
            \\frac{\\partial \\loss}{\\partial \\mathbf{z}^{(l)}}
            (\\mathbf{x}^{(l-1)})\\transpose \\\\
            \\frac{\\partial \\loss}{\\partial \\bias^{(l)}} &=
            \\frac{\\partial \\loss}{\\partial \\mathbf{z}^{(l)}} \\\\
            \\frac{\\partial \\loss}{\\partial \\mathbf{x}^{(l-1)}} &=
            (\\weight^{(l)})\\transpose \\frac{\\partial \\loss}{\\partial \\mathbf{z}^{(l)}}
            \\end{align}

    Common Activation Functions:
        * **ReLU**: :math:`\\relu(x) = \\max(0, x)`
        * **Sigmoid**: :math:`\\sigmoid(x) = \\frac{1}{1 + e^{-x}}`
        * **Tanh**: :math:`\\tanh(x) = \\frac{e^x - e^{-x}}{e^x + e^{-x}}`
        * **Softmax**: :math:`\\softmax(x_i) = \\frac{e^{x_i}}{\\sum_{j=1}^K e^{x_j}}`

    Args:
        layer_sizes: List of layer dimensions :math:`[d_0, d_1, ..., d_L]`
            where :math:`d_0` is input dimension and :math:`d_L` is output dimension.
        activation: Activation function name. Supported: 'relu', 'sigmoid', 'tanh'.

    Example:
        Create a 3-layer network for classification:

        >>> mlp = MultiLayerPerceptron(
        ...     layer_sizes=[784, 128, 64, 10],  # MNIST-like architecture
        ...     activation='relu'
        ... )
        >>> output = mlp.forward(input_batch)
        >>> loss = mlp.compute_loss(output, targets)
        >>> mlp.backward(loss)

    Mathematical Properties:
        * **Universal Approximation**: MLPs with sufficient hidden units can
          approximate any continuous function on compact domains
        * **Parameter Count**: :math:`\\sum_{l=1}^L (d_{l-1} + 1) \\cdot d_l`
        * **Computational Complexity**: :math:`O(\\sum_{l=1}^L d_{l-1} \\cdot d_l)`
          per forward pass
    """
```

## Enhancement Opportunities

### 1. Interactive Mathematical Examples

```python
def add_interactive_math_examples(app):
    """Add interactive mathematical examples using MathJax."""

    def process_interactive_math(app, docname, source):
        """Process interactive math examples."""
        content = source[0]

        # Find interactive math blocks
        import re
        pattern = r'.. interactive-math::\s*\n(.*?)\n\n'

        def replace_interactive_math(match):
            math_content = match.group(1).strip()

            # Generate interactive math HTML
            return f"""
.. raw:: html

   <div class="interactive-math" data-math="{math_content}">
      <div class="math-display">\\[{math_content}\\]</div>
      <div class="math-controls">
         <button onclick="toggleMathSteps(this)">Show Steps</button>
         <button onclick="plotMathFunction(this)">Plot</button>
      </div>
   </div>
"""

        source[0] = re.sub(pattern, replace_interactive_math, content, flags=re.DOTALL)

    app.connect('source-read', process_interactive_math)

    # Add JavaScript for interactivity
    app.add_js_file('interactive-math.js')

def setup(app):
    add_interactive_math_examples(app)
```

### 2. Mathematical Cross-Reference Enhancement

```python
def enhance_math_references(app):
    """Enhance mathematical cross-references."""

    def resolve_math_references(app, env, node, contnode):
        """Resolve enhanced mathematical references."""
        if node.get('reftype') == 'math':
            target = node.get('reftarget')

            # Enhanced math reference with equation preview
            if target in env.math_equations:
                equation = env.math_equations[target]
                tooltip_content = f"Equation {target}: {equation['formula']}"

                # Add tooltip with equation preview
                contnode.attributes['title'] = tooltip_content
                contnode.attributes['class'] = 'math-reference'

        return None

    app.connect('missing-reference', resolve_math_references)

def setup(app):
    enhance_math_references(app)
```

### 3. Mathematical Notation Validation

```python
def validate_mathematical_notation(app):
    """Validate mathematical notation in documentation."""

    def check_math_syntax(app, exception):
        """Check mathematical notation for common errors."""
        if exception:
            return

        math_errors = []

        for docname in app.env.all_docs:
            doc = app.env.get_doctree(docname)

            # Check math nodes for common issues
            for math_node in doc.traverse(math):
                latex_content = math_node.astext()

                # Common LaTeX errors
                if '\\frac{}{' in latex_content:
                    math_errors.append(f"{docname}: Empty numerator in fraction")

                if latex_content.count('{') != latex_content.count('}'):
                    math_errors.append(f"{docname}: Unmatched braces in math")

                # Check for undefined macros
                undefined_macros = find_undefined_macros(latex_content)
                for macro in undefined_macros:
                    math_errors.append(f"{docname}: Undefined macro \\{macro}")

        if math_errors:
            app.warn(f"Mathematical notation errors found: {len(math_errors)}")
            for error in math_errors[:10]:  # Show first 10 errors
                app.warn(f"  {error}")

    app.connect('build-finished', check_math_syntax)

def find_undefined_macros(latex_content):
    """Find undefined macros in LaTeX content."""
    import re

    # Extract all macro usage
    macros_used = re.findall(r'\\([a-zA-Z]+)', latex_content)

    # Known LaTeX commands (subset)
    known_commands = {
        'frac', 'sqrt', 'sum', 'int', 'lim', 'log', 'ln', 'sin', 'cos', 'tan',
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'mu',
        'sigma', 'phi', 'pi', 'mathbb', 'mathcal', 'mathbf', 'operatorname',
        'left', 'right', 'begin', 'end', 'text', 'cdot', 'times', 'approx'
    }

    # Find potentially undefined macros
    undefined = []
    for macro in macros_used:
        if macro not in known_commands and macro not in app.config.mathjax3_config['tex']['macros']:
            undefined.append(macro)

    return list(set(undefined))

def setup(app):
    validate_mathematical_notation(app)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic MathJax rendering** - LaTeX mathematics displays correctly
- [x] **Inline and display math** - Both :math: and .. math:: directives work
- [x] **Equation numbering** - Automatic numbering and referencing
- [x] **Theme integration** - Mathematics matches documentation theme
- [x] **Mobile compatibility** - Mathematical notation works on all devices

### 🔄 Enhancement Opportunities

- [ ] **AI/ML macro library** - Comprehensive mathematical notation for AI/ML
- [ ] **Interactive examples** - Manipulable mathematical expressions
- [ ] **Notation validation** - Automatic checking for mathematical errors
- [ ] **Cross-reference enhancement** - Rich mathematical cross-references
- [ ] **Template integration** - Mathematical notation in AutoAPI templates

### 📋 Template Integration Tasks

1. **Mathematical API templates** for algorithm and model documentation
2. **AI/ML notation macros** for consistent mathematical expressions
3. **Interactive math examples** for enhanced learning
4. **Notation validation** for documentation quality assurance

## Integration with AutoAPI

### Mathematical Function Documentation

```jinja2
{# Render functions with mathematical content #}
{% if obj.has_mathematical_notation %}
.. py:function:: {{ obj.signature }}

   {% if obj.algorithm_description %}
   **Algorithm:**

   {{ obj.algorithm_description|process_math }}
   {% endif %}

   {% if obj.mathematical_formula %}
   **Mathematical Definition:**

   .. math::
      {{ obj.mathematical_formula }}
   {% endif %}

   {% if obj.complexity_analysis %}
   **Complexity:**

   * Time: :math:`{{ obj.complexity_analysis.time }}`
   * Space: :math:`{{ obj.complexity_analysis.space }}`
   {% endif %}
{% endif %}
```

### Mathematical Model Classes

```jinja2
{# Enhanced class documentation for mathematical models #}
{% if obj.is_mathematical_model %}
<div class="mathematical-model">
   <h2>{{ obj.name }}</h2>

   {% if obj.mathematical_foundation %}
   <div class="math-foundation">
      <h3>Mathematical Foundation</h3>
      {{ obj.mathematical_foundation|process_math }}
   </div>
   {% endif %}

   {% if obj.key_equations %}
   <div class="key-equations">
      <h3>Key Equations</h3>
      {% for eq in obj.key_equations %}
      <div class="equation-block">
         .. math::
            :label: {{ eq.label }}

            {{ eq.formula }}

         {{ eq.description }}
      </div>
      {% endfor %}
   </div>
   {% endif %}
</div>
{% endif %}
```

## Performance Considerations

### MathJax Loading Optimization

```python
# Optimize MathJax loading for better performance
mathjax3_config['loader']['load'] = ['input/tex', 'output/svg']  # Only load needed components
mathjax3_config['svg']['fontCache'] = 'global'  # Cache fonts globally
mathjax3_config['options']['skipHtmlTags'] = ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
```

### Build Time Considerations

```python
# For development builds, use faster MathJax configuration
import os
if os.environ.get('FAST_BUILD'):
    mathjax3_config['svg']['scale'] = 0.8  # Smaller scale for faster rendering
    mathjax3_config['options']['enableMenu'] = False  # Disable menu for speed
```

## Troubleshooting

### Common Issues

1. **Math Not Rendering**: Check MathJax CDN availability and configuration
2. **Macro Errors**: Verify custom macros are properly defined
3. **Mobile Display Issues**: Ensure responsive configuration is enabled
4. **Performance Problems**: Consider local MathJax for offline builds

### Debug Configuration

```python
# Debug MathJax processing
mathjax3_config['options']['showMathMenu'] = True
mathjax3_config['startup']['ready'] = "() => { console.log('MathJax loaded'); MathJax.startup.defaultReady(); }"
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), MathJax provides:

1. **Mathematical API Documentation**: Rich mathematical notation in function and class documentation
2. **Algorithm Descriptions**: Clear mathematical representation of algorithms
3. **Statistical Model Documentation**: Comprehensive mathematical foundations for AI/ML models
4. **Interactive Examples**: Enhanced learning through mathematical visualization

MathJax enables AutoAPI templates to create professional-grade mathematical documentation that clearly communicates complex algorithms and mathematical concepts in AI/ML codebases.
