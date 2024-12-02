<template>
    <div class="calendar-container">
        <div class="demo-app-main">
            <FullCalendar class="demo-app-calendar" :options="calendarOptions">
                <template v-slot:eventContent="arg">
                    <div class="event-content" :class="'priority-' + arg.event.extendedProps.priority">
                        <b>{{ arg.timeText }}</b>
                        <i>{{ arg.event.title }}</i>
                    </div>
                </template>
            </FullCalendar>
            <div class="priority-legend">
                <span class="priority-1">รีบ</span>
                <span class="priority-2">ตาม</span>
                <span class="priority-3">นอนทำ</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, watch } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { CalendarOptions, DateSelectArg, EventClickArg } from '@fullcalendar/core';
import * as functions from '../function/function.inc';

const props = defineProps(['selectedDate']); 
const events = ref(functions.INITIAL_EVENTS); 

watch(
    () => props.selectedDate,
    (newValue) => {
        if (newValue) {
            const newEvent = {
                id: functions.createEventId(),
                title: newValue.title,
                start: newValue.start,
                end: newValue.end,
                allDay: true, 
                priority: newValue.priority || 1
            };
            events.value.push(newEvent); 
        }
    },
    { immediate: true } 
);

const calendarOptions = ref<CalendarOptions>({
    plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
    headerToolbar: { left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,timeGridDay' },
    initialView: 'dayGridMonth',
    events: events.value,
    editable: true,
    selectable: true,
    select: (selectInfo: DateSelectArg) => {
        let title = prompt('Please enter a new title for your event');
        let calendarApi = selectInfo.view.calendar;
        calendarApi.unselect();

        if (title) {
            const newEvent = {
                id: functions.createEventId(),
                title,
                start: selectInfo.startStr,
                end: selectInfo.endStr,
                allDay: selectInfo.allDay,
                priority: 1 

            };
            events.value.push(newEvent); 
            calendarApi.addEvent(newEvent); 
        }
    },
    eventClick: (clickInfo: EventClickArg) => {
        if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
            clickInfo.event.remove();
            events.value = events.value.filter(event => event.id !== clickInfo.event.id); 
        }
    }
});
</script>

<style lang="scss" scoped>
.calendar-container {
    background-color: #ffffff;
    margin-top: 1rem;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

.demo-app-main {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.demo-app-calendar {
    flex: 1;
    min-height: 0;
    overflow: hidden;
}

.priority-legend {
    display: flex;
}

.priority-1 {
    background-color: #ffcccc;
}

.priority-2 {
    background-color: #ffe4b3;
}

.priority-3 {
    background-color: #d1e7dd;
}

.event-content {
    padding: 4px;
    background-color: #f1f1f1;

    &.priority-1 {
        background-color: #ffcccc;
    }

    &.priority-2 {
        background-color: #ffe4b3;
    }

    &.priority-3 {
        background-color: #d1e7dd;
    }
}

.fc-event-main{
    &.priority-1 {
        &.fc-event-main{
            background-color: #ffcccc;

        }
        background-color: #ffcccc;
    }

    &.priority-2 {
        background-color: #ffe4b3;
    }

    &.priority-3 {
        background-color: #d1e7dd;
    }
}
</style>
