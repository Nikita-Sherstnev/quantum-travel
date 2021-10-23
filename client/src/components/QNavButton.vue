<template>
  <div
    class="q-nav-button"
    :class="{ active }"
    :style="{ ['--q-bg-color']: `#${color}` }"
  >
    <div class="q-nav-button__icon" :class="{ active }">
      <i :class="icon"></i>
    </div>
    <div class="q-nav-button__label">{{ label }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "QNavButton",
  props: {
    icon: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      required: true,
    },
    active: {
      type: Boolean,
      required: true,
    },
  },
});
</script>

<style scoped lang="scss">
.q-nav-button {
  display: block;
  position: relative;
  cursor: pointer;

  &.active:after {
    position: absolute;
    display: block;
    content: "";
    height: 4px;
    width: 30px;
    background: var(--q-bg-color);
    bottom: -8px;
    border-radius: 5px;
    left: calc(50% - 15px);
    box-shadow: 0 0 10px 0 var(--q-bg-color);
    transition: 250ms;
  }

  &__icon {
    height: 45px;
    width: 45px;
    box-sizing: border-box;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    background: var(--q-bg-color);
    border: 3px solid var(--q-bg-color);
    margin: 0 auto;
    box-shadow: 0 2px 10px 0 rgba(#000, 0.15);
    transition: 250ms;

    &.active,
    &:hover {
      color: var(--q-bg-color);
      background: #fff;
      box-shadow: 0 0 10px -2px var(--q-bg-color);
    }
  }

  &__label {
    height: 25px;
    line-height: 25px;
    width: 100%;
    font-size: 0.9em;
    text-transform: capitalize;
    padding-top: 3px;
  }
}
</style>
