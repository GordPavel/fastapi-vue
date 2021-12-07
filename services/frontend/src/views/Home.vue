<template>
  <section>
    <div class="container">
      <div>Hello to quadratic equations solver</div>
      <div>Here you can enter the coefficients of quadratic equation and this service will solve the roots</div>
      <div>Please, enter a, b, c coefficients of equation in form
        <span class="equation" v-katex="'a \\times x^2 + b \\times x + c = 0'"></span>
      </div>
      <div v-if="error" class="alert alert-danger" role="alert">
        Sorry, error happen. Please try again.
      </div>
      <form @submit.prevent="solve_equation">
        <div style="margin: 10px">
          <div class="row align-items-start">
            <div class="col">
              <label for="a-coef" class="form-label">a:</label>
              <input type="text" id="a-coef" v-model.number="a" class="form-control" :disabled="is_loading"/>
            </div>
            <div class="col">
              <label for="b-coef" class="form-label">b:</label>
              <input type="text" id="b-coef" v-model.number="b" class="form-control" :disabled="is_loading"/>
            </div>
            <div class="col">
              <label for="c-coef" class="form-label">c:</label>
              <input type="text" id="c-coef" v-model.number="c" class="form-control" :disabled="is_loading"/>
            </div>
          </div>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="is_loading">Solve</button>
      </form>
      <div v-if="roots !== null" style="margin: 10px">
        Roots: <span>{{ roots }}</span>
        <div>
          <button type="submit" @click.prevent="draw_plot" v-if="plot === null" class="btn btn-primary"
                  :disabled="is_loading">Show plot
          </button>
          <div v-if="plot_error" class="alert alert-danger" role="alert">
            No real roots to show the plot. Try another coefficients.
          </div>
          <img v-if="plot !== null" :src="'data:image/jpeg;base64,'+plot" alt="plot"/>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import Vue from 'vue'
import axios from 'axios';
import VueKatex from 'vue-katex'

Vue.use(VueKatex)
export default {
  name: 'Home',
  data() {
    return {
      is_loading: false,
      a: 0.0,
      b: 0.0,
      c: 0.0,
      roots: null,
      plot: null,
      error: false,
      plot_error: false,
    };
  },
  methods: {
    async solve_equation() {
      const comp = this
      comp.is_loading = true
      comp.plot = null
      comp.error = false
      comp.plot_error = false
      axios
          .get('/solve', {
            params: {
              'a': comp.a,
              'b': comp.b,
              'c': comp.c,
            }
          })
          .catch(() => {
            comp.error = true
          })
          .then(response => {
            comp.roots = response.data.roots
          })
          .finally(() => {
            comp.is_loading = false
          });
    },
    async draw_plot() {
      const comp = this
      comp.is_loading = true
      comp.error = false
      comp.plot_error = false
      axios
          .get('/get_plot', {
            params: {
              'a': comp.a,
              'b': comp.b,
              'c': comp.c,
            }
          })
          .catch(() => {
            comp.error = true
          })
          .then(response => {
            if (response.data.success) {
              comp.plot = response.data.plot
            } else {
              comp.plot_error = true
            }
          })
          .finally(() => {
            comp.is_loading = false
          });
    }
  },

}
</script>
