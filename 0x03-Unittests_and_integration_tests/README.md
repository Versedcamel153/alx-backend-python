## ✅ 1. Difference Between Unit and Integration Tests

### 🧪 Unit Tests
- **Definition**: Unit tests check individual parts (units) of your code in isolation.
- **Goal**: To ensure that a single function, method, or class works as expected.
- **Example**: Testing `access_nested_map()` to make sure it returns the correct value or raises `KeyError` when it should.
- **Key Point**: No dependencies like databases, APIs, or the internet are involved — you isolate the logic.

🔍 Think of unit tests as testing each LEGO brick to make sure it's not broken.

### 🔗 Integration Tests
- **Definition**: Integration tests check how multiple components of your system work together.
- **Goal**: To ensure that the combination of parts behaves correctly when integrated.
- **Example**: Testing `GithubOrgClient.public_repos()` with real payloads to simulate actual GitHub API data (while still mocking external requests).
- **Key Point**: They may involve mock APIs or data, but they test full workflows rather than small pieces.

🧱 Think of integration tests as checking whether the LEGO bricks fit together to build a proper house.

## ✅ 2. Common Testing Patterns

### 🔄 Mocking
- **What it is**: Replacing real objects or functions (like API calls) with fake ones that return controlled results.
- **Why it's useful**: To avoid relying on external services like GitHub or the internet in your tests.
- **Example**:

```python
@patch('client.get_json')
def test_org(self, mock_get_json):
    mock_get_json.return_value = {"login": "google"}
```

🧪 Mocking lets you simulate any situation (errors, responses, delays) without needing the real thing.

### ⚙️ Parametrization
- **What it is**: Running the same test logic with multiple input values.
- **Why it's useful**: Reduces repeated code and ensures your logic works across different cases.
- **Example**:

```python
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
```

📦 Parametrization = one test function, many scenarios.

### 🧰 Fixtures
- **What it is**: Predefined test data or setup used in multiple tests.
- **Why it's useful**: Ensures consistency and makes integration tests realistic without depending on live data.
- **Example**: `TEST_PAYLOAD` in `fixtures.py` provides mock GitHub API responses for use in multiple tests.

🛠 Fixtures are like mock environments — reusable setups to test against.

## ✅ Summary Table

| Concept          | Purpose                               | Example in Project              |
|------------------|----------------------------------------|----------------------------------|
| Unit Test        | Test small, isolated code units        | `test_access_nested_map`         |
| Integration Test | Test combined components or workflows  | `TestIntegrationGithubOrgClient` |
| Mocking          | Simulate external calls or objects     | `@patch('client.get_json')`      |
| Parametrization  | Run same test with different inputs    | `@parameterized.expand([...])`   |
| Fixtures         | Predefined data used in tests          | `TEST_PAYLOAD` in `fixtures.py`  |
