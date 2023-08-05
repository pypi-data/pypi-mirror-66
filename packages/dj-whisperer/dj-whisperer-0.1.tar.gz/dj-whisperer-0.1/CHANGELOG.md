# 0.1

* First PyPI release

## Backwards incompatible changes

* `deliver_event` is no longer provided directly from the `whisperer` module. Please refactor your imports as:

  ```python
  from whisperer.tasks import deliver_event
  ```

* `registry` is no longer provided directly from the `whisperer` module. Please refactor your imports as:

  ```python
  from whisperer.events import registry
  ```
