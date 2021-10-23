<template>
  <div class="q-route-card">
    <div class="q-route-card__img"></div>
    <div class="q-route-card__name">{{ name }}</div>
    <ul class="q-route-card__list">
      <li v-for="item in items" :key="item.id" class="q-route-card__item">
        <div class="q-route-card__item-name">{{ item.name }}</div>
        <div class="q-route-card__item-desc">{{ item.description }}</div>
      </li>
    </ul>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Item } from "@/views/Home.vue";

export default defineComponent({
  name: "QRouteCard",
  props: {
    name: {
      type: String,
      required: true,
    },
    items: {
      type: Object as PropType<Item[]>,
      required: true,
    },
  },
});
</script>

<style scoped lang="scss">
.q-route-card {
  &__name {
    font-size: 1.1em;
    text-transform: capitalize;
  }
}
</style>
