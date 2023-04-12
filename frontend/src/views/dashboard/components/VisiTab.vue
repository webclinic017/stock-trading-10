<template>
  <div class="mt-4">
    <NRow :gutter="24">
      <NCol :span="24">
        <n-card content-style="padding: 0;" :bordered="false">
          <n-tabs type="line" size="large" :tabs-padding="20" pane-style="padding: 20px;">
            <n-tab-pane name="上证指数">
              <shCompositeIndex />
            </n-tab-pane>
            <n-tab-pane name="沪深300">
              <Csi300 />
            </n-tab-pane>
          </n-tabs>
        </n-card>
      </NCol>
    </NRow>
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import shCompositeIndex from '@/views/dashboard/components/ShCompositeIndex.vue';
  import Csi300 from '@/views/dashboard/components/Csi300.vue';

  export default defineComponent({
    components: { shCompositeIndex, Csi300 },
    setup() {
      return {};
    },
  });
</script>
