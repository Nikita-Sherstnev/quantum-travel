<template>
  <div class="q-home">
    <q-map class="q-home__map" @select="select"></q-map>
    <div class="q-home__right q-right" v-if="isShow">
      <div class="q-right__title">
        <i class="fas fa-subway"></i>
        {{ selected.ref.name }}
      </div>

      <nav class="q-right__nav">
        <q-nav-button
          icon="fas fa-utensils"
          label="кафе"
          color="ffbf13"
          :active="currentTab === 'food'"
          @click="() => nav('food')"
        ></q-nav-button>
        <q-nav-button
          icon="fas fa-landmark"
          label="интересно"
          color="6C3DF1FF"
          :active="currentTab === 'interesting'"
          @click="() => nav('interesting')"
        ></q-nav-button>
        <q-nav-button
          icon="fas fa-running"
          label="спорт"
          color="81d33f"
          :active="currentTab === 'sport'"
          @click="() => nav('sport')"
        ></q-nav-button>
      </nav>

      <div class="q-right__input-wrapper">
        <i class="fas fa-search q-right__input-icon"></i>
        <input type="text" class="q-right__input" v-model="search" />
      </div>

      <div class="q-right__items">
        <q-item-card
          v-for="item in data"
          :key="item.id"
          :name="item.name"
          :desc="item.description"
          :active="isActive(item.id)"
          @click="() => togglePlace(item)"
        />
      </div>
    </div>
    <div class="q-home__left q-left" v-if="isShow">
      <div class="q-left__title">
        <i class="fas fa-route"></i>
        Ваш маршрут
      </div>

      <div class="q-left__route">
        <el-timeline v-if="route.length !== 0">
          <el-timeline-item
            v-for="(item, index) in route"
            :key="index"
            timestamp="10 минут"
            placement="top"
            color="#FF6A00"
          >
            <q-route-card
              :name="item"
              :items="
                places
                  .filter((el) => el.metro.name === item)
                  .map((el) => el.item)
              "
            ></q-route-card>
          </el-timeline-item>
        </el-timeline>
        <div class="q-left__none" v-else>
          <el-empty description="Вы ничего не выбрали"></el-empty>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, ref } from "vue";
import QMap from "@/components/QMap.vue";
import QItemCard from "@/components/QItemCard.vue";
import QNavButton from "@/components/QNavButton.vue";
import QRouteCard from "@/components/QRouteCard.vue";

export interface Item {
  id: number;
  name: string;
  description: string;
}

interface Station {
  name: string;
  coords: number[];
}

export default defineComponent({
  name: "Home",
  components: { QRouteCard, QNavButton, QItemCard, QMap },
  setup() {
    const selected = reactive({ ref: { name: "", coords: [] as number[] } });

    const dataFood = ref([] as Item[]);
    const dataInteresting = ref([] as Item[]);
    const dataSport = ref([] as Item[]);

    const data = computed(() => {
      let locData = [];
      if (currentTab.value === "food") {
        locData = dataFood.value;
      } else if (currentTab.value === "interesting") {
        locData = dataInteresting.value;
      } else {
        locData = dataSport.value;
      }

      return locData
        .filter(
          (item) =>
            item.name.includes(search.value) ||
            item.description.includes(search.value)
        )
        .filter(
          (item) =>
            places.value.filter((el) => el.item.id === item.id).length === 0 ||
            places.value.filter(
              (el) =>
                el.item.id === item.id && selected.ref.name === el.metro.name
            ).length === 1
        );
    });

    const search = ref("");

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

    const select = (e: Station) => {
      selected.ref = e;
      load("кафе", e.coords, (data) => (dataFood.value = data));
      load(
        "достопримечательности",
        e.coords,
        (data) => (dataInteresting.value = data)
      );
      load("спорт", e.coords, (data) => (dataSport.value = data));
    };

    const currentTab = ref<"food" | "interesting" | "sport">("food");
    const nav = (val: "food" | "interesting" | "sport") => {
      currentTab.value = val;
    };

    const places = ref<{ item: Item; metro: Station }[]>([]);

    const isActive = (id: number) => {
      return places.value.filter((item) => item.item.id === id).length === 1;
    };

    const togglePlace = (newItem: Item) => {
      if (
        places.value.filter((item) => item.item.id === newItem.id).length > 0
      ) {
        places.value = places.value.filter(
          (item) => item.item.id !== newItem.id
        );
      } else {
        places.value.push({ item: newItem, metro: selected.ref });
      }
    };

    const route = computed<string[]>(() => {
      return [...new Set(places.value.map((item) => item.metro.name))];
    });

    console.log(route);

    const isShow = computed(() => {
      return selected.ref.name !== "" || true;
    });

    return {
      selected,
      select,
      dataFood,
      data,

      route,

      isShow,

      search,

      places,
      togglePlace,
      isActive,

      currentTab,
      nav,
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

  &__right,
  &__left {
    height: calc(100% - 70px);
    width: 340px;
    z-index: 999;
    position: absolute;
  }

  &__right {
    top: 15px;
    right: 15px;
  }

  &__left {
    top: 15px;
    left: 15px;
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

  &__route {
    margin-top: 20px;
    height: calc(100% - 50px);
    width: 100%;
  }

  &__none {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

.q-right {
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
    margin: 20px auto 15px auto;
  }

  &__items {
    height: calc(100% - 115px);
    overflow-y: auto;
  }

  &__input-wrapper {
    height: 36px;
    width: 100%;
    position: relative;
    box-sizing: border-box;
    margin: 22px auto 12px auto;
  }

  &__input-icon {
    position: absolute;
    top: 12px;
    left: 12px;
    color: rgba(#000, 0.6);
  }

  &__input {
    width: calc(100% - 45px);
    height: calc(100% - 4px);
    border-radius: 12px;
    outline: none;
    border: 1px solid rgba(#000, 0.15);
    box-shadow: 0 2px 5px 0 rgba(#000, 0.15);
    padding: 2px 5px 2px 40px;
    font-weight: 500;
    font-size: 1.1em;
    transition: 250ms;

    &:focus {
      border: 1px solid rgba(#269ef1, 0.7);
      box-shadow: 0 1px 3px 0 rgba(#000, 0.25);
    }
  }
}
</style>
