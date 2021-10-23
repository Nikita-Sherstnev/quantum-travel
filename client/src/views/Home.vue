<template>
  <div class="q-home">
    <q-map class="q-home__map" @select="select"></q-map>
    <div class="q-home__left q-left" v-if="selected.ref.name !== ''">
      <div class="q-left__title">
        {{ selected.ref.name }}
      </div>

      <nav class="q-left__nav">
        <q-nav-button
          icon="fas fa-utensils"
          label="кафе"
          color="ffbf13"
          @click="() => nav('food')"
        ></q-nav-button>
        <q-nav-button
          icon="fas fa-landmark"
          label="интересно"
          color="6C3DF1FF"
          @click="() => nav('interesting')"
        ></q-nav-button>
        <q-nav-button
          icon="fas fa-running"
          label="спорт"
          color="81d33f"
          @click="() => nav('sport')"
        ></q-nav-button>
      </nav>

      <div class="q-left__items">
        <q-item-card
          v-for="item in data"
          :key="item.id"
          :name="item.name"
          :desc="item.description"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, ref } from "vue";
import QMap from "@/components/QMap.vue";
import QItemCard from "@/components/QItemCard.vue";
import QNavButton from "@/components/QNavButton.vue";

interface Item {
  id: number;
  name: string;
  description: string;
}

export default defineComponent({
  name: "Home",
  components: { QNavButton, QItemCard, QMap },
  setup() {
    const selected = reactive({ ref: { name: "", coords: [] as number[] } });

    const data = ref([] as Item[]);
    const dataFood = ref([] as Item[]);
    const dataInteresting = ref([] as Item[]);
    const dataSport = ref([] as Item[]);

    const dataFinal = computed(() => {
      if (data.value.length === 0) {
        return data;
      }
      return dataFood;
    });

    const load = (
      text: string,
      coords: number[],
      callback: (data: Item[]) => void
    ) => {
      fetch(
        `https://search-maps.yandex.ru/v1/?text=${text}&spn=0.552069,0.400552&ll=${coords[1]},${coords[0]}&results=10&lang=ru_RU&apikey=29ce5500-d711-4d9b-a977-e1d7d80d5394`
      )
        .then((res) => {
          return res.json();
        })
        .then((res) => {
          callback(
            res.features.map(
              (item: any) =>
                ({
                  id: item.properties.CompanyMetaData.id,
                  name: item.properties.name,
                  description: item.properties.description,
                } as Item)
            )
          );
        });
    };

    const select = (e: { name: string; coords: number[] }) => {
      selected.ref = e;
      load("кафе", e.coords, (data) => (dataFood.value = data));
      load(
        "достопримечательности",
        e.coords,
        (data) => (dataInteresting.value = data)
      );
      load("спорт", e.coords, (data) => (dataSport.value = data));
    };

    const nav = (val: string) => {
      if (val === "food") {
        data.value = dataFood.value;
      } else if (val === "interesting") {
        data.value = dataInteresting.value;
      } else if (val === "sport") {
        data.value = dataSport.value;
      }
    };

    return {
      selected,
      select,
      dataFood,
      data,
      nav,
      dataFinal,
    };
  },
});
</script>

<style scoped lang="scss">
.q-home {
  width: 100%;
  height: 100%;
  display: block;
  position: relative;

  &__map {
    width: 100%;
    height: 100%;
    position: relative;
  }

  &__left {
    position: absolute;
    top: 15px;
    right: 15px;
    height: calc(100% - 70px);
    width: 340px;
    z-index: 999;
  }
}

.q-left {
  background: #fff;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 2px 2px 15px 0 rgba(#000, 0.25);
  overflow: hidden;

  &__title {
    font-weight: bolder;
    text-transform: capitalize;
    font-size: 1.3em;
    text-align: center;
  }

  &__nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 20px auto 5px auto;
  }

  &__items {
    height: calc(100% - 105px);
    overflow-y: auto;
  }
}
</style>
