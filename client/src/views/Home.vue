<template>
  <div class="q-home">
    <q-map class="q-home__map" @select="select"></q-map>

    <div class="q-home__right q-right" :class="{ show: isShow }">
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

    <div class="q-home__left q-left" :class="{ show: isShow }">
      <div class="q-left__title">
        <i class="fas fa-route"></i>
        Ваш маршрут
      </div>

      <div class="q-left__route">
        <el-timeline v-if="route.length !== 0">
          <el-timeline-item
            v-for="(item, index) in isCalculated ? calculatedRoute : route"
            :key="index"
            :timestamp="isCalculated ? `${item.time} минут` : '### минут'"
            placement="top"
            :color="isCalculated ? '#FF6A00' : '#949494'"
          >
            <q-route-card
              :name="isCalculated ? item.name : item"
              :items="
                places
                  .filter((el) => el.metro.name === (isCalculated ? item.name : item))
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

    <div class="q-home__app-bar q-app-bar" v-if="!dialogVisible">
      <div class="q-app-bar__expected-time">
        <span class="label">Ожидаемое время:</span>{{ expectedTime }}
      </div>
      <div class="q-app-bar__wanted-time">
        <span class="label">Желаемое время:</span>{{ wantedTime }}
      </div>
    </div>

    <div class="q-home__footer q-footer">
      <img src="../assets/logo.svg" alt="logo" class="q-footer__logo" />
      <div class="q-footer__text">Цифровой прорыв 2021 - РОСАТОМ</div>
    </div>
  </div>

  <el-dialog
    v-model="dialogVisible"
    title="Добро пожаловать!"
    width="30%"
    center
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="false"
  >
    <div class="q-welcome">
      <img src="../assets/1.svg" alt="Welcome!" class="q-welcome__art" />
      <div class="q-welcome__text">
        Сколько времени вы планируете потратить на посещение<br />
        достопримечательностей?
      </div>
      <input type="time" v-model="wantedTime" class="q-welcome__input" />
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="warning" @click="start"> Начать </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, ref, watch } from "vue";
import QMap from "@/components/QMap.vue";
import QItemCard from "@/components/QItemCard.vue";
import QNavButton from "@/components/QNavButton.vue";
import QRouteCard from "@/components/QRouteCard.vue";
import moment from "moment";

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
        `https://search-maps.yandex.ru/v1/?text=${text}&spn=0.552069,0.400552&ll=${coords[1]},${coords[0]}&results=10&lang=ru_RU&apikey=28fa19de-4f0a-44b5-93c2-8a8d3f0efa8e`
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

    const isShow = computed(() => {
      return selected.ref.name !== "";
    });

    const sendData = async () => {
      let mtrx: number[][] = [];
      let cnt = 0;

      for (let i = 0; i < route.value.length; i++) {
        for (let j = i + 1; j < route.value.length; j++) {
          cnt++;
          let multiRoute = new (window as any).ymaps.multiRouter.MultiRoute({
            referencePoints: [route.value[i], route.value[j]],
            params: {
              routingMode: "masstransit",
            },
          });

          multiRoute.model.events.add("requestsuccess", function () {
            let activeRoute = multiRoute.getActiveRoute();
            let mins = 15;

            if (!activeRoute) {
              mins = 15;
            }
            mtrx.push([
              i,
              j,
              parseInt(
                activeRoute
                  ? activeRoute.properties.get("duration").text.split(" ")[0]
                  : mins
              ),
            ]);
          });
        }
      }

      while (mtrx.length !== cnt) {
        await new Promise((resolve) => setTimeout(resolve, 500));
      }

      const res = await fetch("/graph", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ graph: mtrx }),
      })
        .then((res) => res.json())
        .then((res) => res.data);

      isCalculated.value = true;
      let locRoutes: { name: string; time: number }[] = [];

      locRoutes.push({ name: route.value[res[0]], time: 0 });

      let gTime = 0;

      for (let i = 1; i < res.length; i++) {
        let time = mtrx.filter(
          (item) =>
            (item[0] === res[i - 1] && item[1] === res[i]) ||
            (item[0] === res[i] && item[1] === res[i - 1])
        )[0][2];
        gTime += time;
        locRoutes.push({
          name: route.value[res[i]],
          time,
        });
      }

      calculatedRoute.value = locRoutes;
      calculatedTime.value = gTime + places.value.length * 30;
    };

    const calculatedRoute = ref<{ name: string; time: number }[]>([]);
    const calculatedTime = ref(0);

    const dialogVisible = ref(true);
    const wantedTime = ref("");
    const start = () => {
      if (wantedTime.value) {
        dialogVisible.value = false;
      }
    };
    const isCalculated = ref(false);
    const expectedTime = computed(() => {
      return isCalculated.value
        ? moment("00:00", "h:mm")
            .add(calculatedTime.value, "minutes")
            .format("h:mm")
        : "00:00";
    });

    watch(
      () => route,
      (val) => {
        if (val.value.length >= 5) {
          sendData();
        }
      },
      { deep: true }
    );

    return {
      selected,
      select,
      dataFood,
      data,

      route,
      calculatedRoute,

      dialogVisible,
      wantedTime,
      start,
      expectedTime,
      isCalculated,

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
  }

  &__right,
  &__left {
    position: absolute;
    z-index: 999;
    width: 340px;
    height: calc(100% - 60px);
    top: 15px;
    transition: 400ms;
  }

  &__right {
    right: -500px;

    &.show {
      right: 15px;
    }
  }

  &__left {
    left: -500px;

    &.show {
      left: 15px;
    }
  }

  &__app-bar {
    position: absolute;
    z-index: 999;
    left: calc(50% - 300px);
    height: 100px;
    width: 600px;
    top: 15px;
  }

  &__footer {
    position: absolute;
    z-index: 999;
    height: 80px;
    width: 600px;
    bottom: 15px;
    left: calc(50% - 300px);
  }
}

.q-app-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;

  &__expected-time,
  &__wanted-time {
    height: 70px;
    line-height: 35px;
    width: 120px;
    font-weight: 500;
    font-size: 38px;
    border-radius: 18px;
    background: #fff;
    text-align: center;
    color: #555555;
    text-shadow: 1px 1px 3px rgba(#555555, 0.15);
    box-shadow: 2px 2px 15px 0 rgba(#000, 0.25);
    flex-direction: column;
    display: flex;

    .label {
      height: 20px;
      line-height: 20px;
      font-weight: normal;
      font-size: 11px;
      text-align: left;
      padding: 5px 10px;
    }
  }
}

.q-welcome {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;

  &__art {
    height: 400px;
    width: 400px;
  }

  &__text {
    text-align: center;
    width: 400px;
    margin: 15px auto;
  }

  &__input {
    width: 150px;
    height: 30px;
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

.q-footer {
  display: flex;
  justify-content: center;
  align-items: center;

  &__text {
    height: 40px;
    width: 450px;
    line-height: 40px;
    font-size: 22px;
    text-align: center;
    color: #555555;
    text-shadow: 1px 1px 3px rgba(#555555, 0.15);
    box-shadow: 2px 2px 15px 0 rgba(#000, 0.25);
    background: #fff;
    border-radius: 12px;
    padding: 3px;
    user-select: none;
    margin: 0 20px;
  }

  &__logo {
    margin: 0 20px;
    height: 80px;
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
