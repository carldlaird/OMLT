from omlt.io.onnx import load_onnx_neural_network
import onnx
import onnxruntime as ort
import numpy as np
import pytest
from pyomo.environ import *

from omlt import OffsetScaling, OmltBlock
from omlt.neuralnet import NeuralNetworkFormulation


def test_onnx_relu(datadir):
    neural_net = onnx.load(datadir.file("keras_linear_131_relu.onnx"))

    model = ConcreteModel()

    scale_x = (1, 0.5)
    scale_y = (-0.25, 0.125)

    scaler = OffsetScaling(
        offset_inputs=[scale_x[0]],
        factor_inputs=[scale_x[1]],
        offset_outputs=[scale_y[0]],
        factor_outputs=[scale_y[1]],
    )

    scaled_input_bounds = {0: (-4, 5) }
    net = load_onnx_neural_network(neural_net, scaler, input_bounds=scaled_input_bounds)
    formulation = NeuralNetworkFormulation(net)
    model.nn = OmltBlock()
    model.nn.build_formulation(formulation)
    
    @model.Objective()
    def obj(mdl):
        return 1

    net_regression = ort.InferenceSession(datadir.file("keras_linear_131_relu.onnx"))

    for x in [-0.25, 0.0, 0.25, 1.5]:
        model.nn.inputs.fix(x)
        result = SolverFactory("cbc").solve(model, tee=False)

        x_s = (x - scale_x[0]) / scale_x[1]
        x_s = np.array([[x_s]], dtype=np.float32)
        outputs = net_regression.run(None, {'dense_input:0': x_s})
        y_s = outputs[0][0, 0]
        y = y_s * scale_y[1] + scale_y[0]

        assert value(model.nn.outputs[0]) == pytest.approx(y)

def test_onnx_linear(datadir):
    neural_net = onnx.load(datadir.file("keras_linear_131.onnx"))

    model = ConcreteModel()

    scale_x = (1, 0.5)
    scale_y = (-0.25, 0.125)

    scaler = OffsetScaling(
        offset_inputs=[scale_x[0]],
        factor_inputs=[scale_x[1]],
        offset_outputs=[scale_y[0]],
        factor_outputs=[scale_y[1]],
    )

    scaled_input_bounds = {0: (-4, 5) }
    net = load_onnx_neural_network(neural_net, scaler, input_bounds=scaled_input_bounds)
    formulation = NeuralNetworkFormulation(net)
    model.nn = OmltBlock()
    model.nn.build_formulation(formulation)
    
    @model.Objective()
    def obj(mdl):
        return 1

    net_regression = ort.InferenceSession(datadir.file("keras_linear_131.onnx"))

    for x in [-0.25, 0.0, 0.25, 1.5]:
        model.nn.inputs.fix(x)
        result = SolverFactory("cbc").solve(model, tee=False)

        x_s = (x - scale_x[0]) / scale_x[1]
        x_s = np.array([[x_s]], dtype=np.float32)
        outputs = net_regression.run(None, {'dense_input:0': x_s})
        y_s = outputs[0][0, 0]
        y = y_s * scale_y[1] + scale_y[0]

        assert value(model.nn.outputs[0]) == pytest.approx(y)

def test_onnx_sigmoid(datadir):
    neural_net = onnx.load(datadir.file("keras_linear_131_sigmoid.onnx"))

    model = ConcreteModel()

    scale_x = (1, 0.5)
    scale_y = (-0.25, 0.125)

    scaler = OffsetScaling(
        offset_inputs=[scale_x[0]],
        factor_inputs=[scale_x[1]],
        offset_outputs=[scale_y[0]],
        factor_outputs=[scale_y[1]],
    )

    scaled_input_bounds = {0: (-4, 5) }
    net = load_onnx_neural_network(neural_net, scaler, input_bounds=scaled_input_bounds)
    formulation = NeuralNetworkFormulation(net)
    model.nn = OmltBlock()
    model.nn.build_formulation(formulation)
    
    @model.Objective()
    def obj(mdl):
        return 1

    net_regression = ort.InferenceSession(datadir.file("keras_linear_131_sigmoid.onnx"))

    for x in [-0.25, 0.0, 0.25, 1.5]:
        model.nn.inputs.fix(x)
        result = SolverFactory("ipopt").solve(model, tee=False)

        x_s = (x - scale_x[0]) / scale_x[1]
        x_s = np.array([[x_s]], dtype=np.float32)
        outputs = net_regression.run(None, {'dense_2_input:0': x_s})
        y_s = outputs[0][0, 0]
        y = y_s * scale_y[1] + scale_y[0]

        assert value(model.nn.outputs[0]) == pytest.approx(y)
