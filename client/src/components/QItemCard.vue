<template>
  <div class="q-item-card" :class="{ active }">
    <div class="q-item-card__img"></div>
    <div class="q-item-card__name">{{ name }}</div>
    <div class="q-item-card__desc">{{ desc }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "QItemCard",
  props: {
    name: {
      type: String,
      required: true,
    },
    desc: {
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
.q-item-card {
  width: calc(100% - 44px);
  height: auto;
  border: 1px solid rgba(#000, 0.1);
  box-shadow: 0 2px 10px 0 rgba(#000, 0.1);
  margin: 15px 7px;
  padding: 15px;
  text-align: left;
  background: #fff;
  transition: 250ms;

  &.active {
    background: rgba(#269ef1, 0.15);
    border: 1px solid rgba(#269ef1, 0.55);
    box-shadow: 0 1px 5px 0 rgba(#000, 0.1);
  }

  &__name {
    font-weight: 500;
    font-size: 1.1em;
    color: #000;
  }

  &__desc {
    color: rgba(#000, 0.6);
  }
}
</style>
