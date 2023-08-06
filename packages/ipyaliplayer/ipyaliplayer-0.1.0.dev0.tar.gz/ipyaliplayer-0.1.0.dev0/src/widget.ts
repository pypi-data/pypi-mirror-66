// Copyright (c) wangsijie
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';
import axios from 'axios';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'

import './aliplayer-components.js'

export
  class PlayerModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: PlayerModel.model_name,
      _model_module: PlayerModel.model_module,
      _model_module_version: PlayerModel.model_module_version,
      _view_name: PlayerModel.view_name,
      _view_module: PlayerModel.view_module,
      _view_module_version: PlayerModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  }

  static model_name = 'PlayerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'PlayerView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

declare global {
  interface Window { [key: string]: any; }
}

const skinLayout = [
  {
    name: 'bigPlayButton',
    align: 'blabs',
    x: 30,
    y: 80,
  },
  {
    name: 'H5Loading',
    align: 'cc',
  },
  {
    name: 'errorDisplay',
    align: 'tlabs',
    x: 0,
    y: 0,
  },
  {
    name: 'infoDisplay',
  },
  {
    name: 'tooltip',
    align: 'blabs',
    x: 0,
    y: 56,
  },
  {
    name: 'thumbnail',
  },
  {
    name: 'controlBar',
    align: 'blabs',
    x: 0,
    y: 0,
    children: [
      {
        name: 'progress',
        align: 'blabs',
        x: 0,
        y: 44,
      },
      {
        name: 'playButton',
        align: 'tl',
        x: 15,
        y: 12,
      },
      {
        name: 'timeDisplay',
        align: 'tl',
        x: 10,
        y: 7,
      },
      {
        name: 'fullScreenButton',
        align: 'tr',
        x: 10,
        y: 12,
      },
      {
        name: 'volume',
        align: 'tr',
        x: 5,
        y: 10,
      },
    ],
  },
];

export
  class PlayerView extends DOMWidgetView {
  private wrapperId?: string;
  render() {
    this.el.htmlContent = '';

    if (!window.Aliplayer) {
      // jQuery的define会导致这里无法正常加载hls组件
      window.__define = window.define;
      window.define = undefined;
      const hm = document.createElement('script');
      hm.src = 'https://g.alicdn.com/de/prismplayer/2.8.2/aliplayer-h5-min.js';
      hm.type = 'text/javascript';
      hm.charset = 'utf-8';
      this.el.appendChild(hm);
    }

    const wrapper = document.createElement('div');
    wrapper.id = `player-con-${Date.now()}`;
    wrapper.className = 'prism-player';
    wrapper.textContent = '正在加载播放器...';
    this.el.appendChild(wrapper);
    this.wrapperId = wrapper.id;

    setTimeout(() => this.renderPlayer(), 100);
    // this.model.on('change:value', this.value_changed, this);
  }

  async getUrls() {
    const vid: string = this.model.get('value');
    // for debug
    if (vid === '27e0590db52c434c8d49cc7678682198') {
      const urls = {
        HD: 'https://ali.videocdn.boyuai.com/27e0590db52c434c8d49cc7678682198/0ca2c54ab046c7aac6d3f4bb05b7342f-ld-encrypt-stream.m3u8',
      };
      return urls;
    }
    const res = await axios.get(`https://www.boyuai.com/common/public-videos/${vid}`);
    return res.data;
  }

  renderPlayer() {
    if (!window.Aliplayer) {
      setTimeout(() => this.renderPlayer(), 100);
    } else {
      this.getUrls().then(urls => {
        if (!Object.keys(urls).length) {
          this.el.textContent = '视频正在转码,请稍后重试';
          return;
        }
        new window.Aliplayer({
          id: this.wrapperId,
          source: JSON.stringify(urls),
          width: this.model.get('_width') + 'px',
          height: this.model.get('_height') + 'px',
          autoplay: false,
          isLive: false,
          rePlay: false,
          playsinline: true,
          preload: false,
          language: 'zh-cn',
          controlBarVisibility: 'hover',
          useH5Prism: true,
          skinLayout,
          components: [
            {
              name: 'RateComponent',
              type: window.AliPlayerComponent.RateComponent,
            },
            {
              name: 'QualityComponent',
              type: window.AliPlayerComponent.QualityComponent,
            },
          ],
        }, () => {
            // 恢复
            window.define = window.__define;
          }
        );
      }).catch(e => {
        console.log(e);
        this.el.textContent = '获取视频播放地址失败';
      })
    }
  }
}
