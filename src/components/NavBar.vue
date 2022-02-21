<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { reactive } from 'vue';

const showBurgerMenu = reactive({ 'is-active': false });

const toggleBurgerMenu = () => {
  showBurgerMenu['is-active'] = !showBurgerMenu['is-active'];
};
</script>
<template>
  <nav
    class="navbar is-primary"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <FontAwesomeIcon icon="fire" class="icon is-medium" />
      </a>
      <a
        role="button"
        class="navbar-burger"
        :class="showBurgerMenu"
        @click.prevent="toggleBurgerMenu"
        aria-label="menu"
        aria-expanded="false"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu" :class="showBurgerMenu">
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-danger">
              <strong>Sign up</strong>
            </a>
            <a class="button is-light"> <strong>Log in</strong> </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
<style lang="scss"></style>
