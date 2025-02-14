import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';
import Vue from 'vue';

import App from './App.vue';
import router from './router';

const hrefRegex = /http:\/\/([\d\w.]+):\d+/;
const groups = hrefRegex.exec(window.location.href);
axios.defaults.baseURL = `http://${groups[1]}:8000/`;  // the FastAPI backend

Vue.config.productionTip = false;

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
