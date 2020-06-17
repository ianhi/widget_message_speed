// Copyright (c) ian
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'


export
class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      value : 'Hello World',
      py_ts_times: []
    };
  }
  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('msg:custom', this._on_msg.bind(this)); 
    this.set('value', 'blarg')//this.get('value')
    // this.set('py_ts_times', [1234]);
    this.save_changes();
  }
  private _on_msg(command: any, buffers: any) {
    if (command.event === 'yikes') {
      // console.log(Date.now() - command.start)
      let times = this.get('py_ts_times');//.concat([Date.now()-command.start]);
      times = times.concat([Date.now() - command.start]);
      // console.log(times);
      this.set('py_ts_times', times);
      this.save_changes();
    } else if (command.event === 'gogogo') {
      this.send({event: 'yikes', start: Date.now()}, [])
    }

  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}


export
class ExampleView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
    this.el.addEventListener('mousemove', this._mouseMove.bind(this));
  }
  _mouseMove(e: MouseEvent) {
      this.model.send({event: 'yikes', start: Date.now()}, [])
    
  }

  value_changed() {
    this.el.textContent = this.model.get('value');
  }
}
