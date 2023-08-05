from typing import Callable, Any, List

from rx.core.typing import Disposable

from rxbp.ack.continueack import continue_ack
from rxbp.observable import Observable
from rxbp.observables.mergeobservable import MergeObservable
from rxbp.observer import Observer
from rxbp.observerinfo import ObserverInfo
from rxbp.scheduler import Scheduler
from rxbp.typing import ElementType


class FlatMergeNoBackpressureObserver(Observer):
    def __init__(
            self,
            observer: Observer,
            selector: Callable[[Any], Observable],
            scheduler: Scheduler,
            subscribe_scheduler: Scheduler,
            is_volatile: bool,
    ):
        self.observer = observer
        self.selector = selector
        self.scheduler = scheduler
        self.subscribe_scheduler = subscribe_scheduler
        self.is_volatile = is_volatile

        self.place_holders = (self.PlaceHolder(), self.PlaceHolder())

        disposable = MergeObservable(
            left=self.place_holders[0],
            right=self.place_holders[1],
        ).observe(ObserverInfo(observer=observer))

    class PlaceHolder(Observable):
        def __init__(self):
            self.observer = None

        def observe(self, observer_info: ObserverInfo) -> Disposable:
            self.observer = observer_info.observer

    def on_next(self, elem: ElementType):
        obs_list: List[Observable] = [self.selector(e) for e in elem]

        for observable in obs_list:
            place_holder = self.PlaceHolder()

            merge_obs = MergeObservable(
                left=observable,
                right=place_holder,
            )

            parent = self.place_holders[0]

            def observe_on_subscribe_scheduler(_, __):
                return merge_obs.observe(ObserverInfo(observer=parent.observer))

            # make sure that Trampoline Scheduler is active
            self.subscribe_scheduler.schedule(observe_on_subscribe_scheduler)

            self.place_holders = (self.place_holders[1], place_holder)

        return continue_ack

    def on_error(self, exc):
        def observe_on_subscribe_scheduler(_, __):
            if self.observer is not None:
                self.observer.on_error(exc)

        self.subscribe_scheduler.schedule(observe_on_subscribe_scheduler)

    def on_completed(self):
        def observe_on_subscribe_scheduler(_, __):
            for place_holder in self.place_holders:
                place_holder.observer.on_completed()

        self.subscribe_scheduler.schedule(observe_on_subscribe_scheduler)
