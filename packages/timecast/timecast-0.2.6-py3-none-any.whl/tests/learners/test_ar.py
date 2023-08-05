"""timecast.learners.AR: testing"""
import flax
import jax
import numpy as onp
import pytest

from timecast.learners import AR


shapes = [(4, 32), (10,), (10, 1), (1,), (1, 10)]


def create_ar(shape, output_features, history_len, history=None):
    """Create AR model"""
    model_def = AR.partial(
        output_features=output_features, history_len=history_len, history=history
    )
    with flax.nn.stateful() as state:
        _, params = model_def.init_by_shape(jax.random.PRNGKey(0), [shape])
        model = flax.nn.Model(model_def, params)
    return model, state


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_features", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_ys_shape(shape, output_features, history_len):
    """Test output shape"""
    model, state = create_ar(shape, output_features, history_len)
    with flax.nn.stateful(state) as _:
        ys = model(onp.random.rand(*shape))

    assert ys.shape == (output_features,)


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_features", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_history_shape(shape, output_features, history_len):
    """Test history shape"""
    model, state = create_ar(shape, output_features, history_len)
    with flax.nn.stateful(state) as state:
        _ = model(onp.random.rand(*shape))

    print(state.as_dict())

    input_features = shape[0] if len(shape) == 1 else shape[1]
    assert state.as_dict()["/"]["history"].shape == (history_len, input_features)


@pytest.mark.parametrize("shape", shapes)
@pytest.mark.parametrize("output_features", [1, 10])
@pytest.mark.parametrize("history_len", [1, 10])
def test_ar_history(shape, output_features, history_len):
    """Test history values"""
    input_features = shape[0] if len(shape) == 1 else shape[1]
    history = onp.random.rand(history_len, input_features)
    model, state = create_ar(shape, output_features, history_len, history)

    onp.testing.assert_array_almost_equal(history, state.as_dict()["/"]["history"])
