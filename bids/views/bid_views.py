# bids/views/bid_views.py
from rest_framework import status, viewsets

from bids.models.bid_model import Bid
from bids.serializers.bid_serializer import BidSerializer
from bids.services.bid_crud_service import BidCRUDService
from core.api_responses.responses import success_response


class BidViewSet(viewsets.GenericViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def list(self, request):
        bids = BidCRUDService.get_bids(
            client=request.query_params.get("client"),
            driver=request.query_params.get("driver"),
            status=request.query_params.get("status"),
        )
        bids = self.filter_queryset(bids)

        return success_response(
            message="Bids retrieved successfully.",
            data=BidSerializer(bids, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        # Your service can raise a DRF NotFound exception,
        # or your global handler can catch Bid.DoesNotExist
        bid = BidCRUDService.get_bid(bid_id=pk)
        return success_response(
            message="Bid retrieved successfully.",
            data=BidSerializer(bid).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = BidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Handled globally!

        validated_data = serializer.validated_data
        if not validated_data.get("client") and request.user.is_authenticated:
            validated_data["client"] = request.user

        bid = BidCRUDService.create_bid(**validated_data)

        return success_response(
            message="Bid created successfully.",
            data=BidSerializer(bid).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        return self._update_bid(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_bid(request, pk, partial=True)

    def _update_bid(self, request, pk, partial):
        bid = BidCRUDService.get_bid(bid_id=pk)
        serializer = BidSerializer(bid, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)  # Handled globally!

        updated_bid = BidCRUDService.update_bid(bid_id=pk, **serializer.validated_data)
        return success_response(
            message="Bid updated successfully.",
            data=BidSerializer(updated_bid).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        BidCRUDService.delete_bid(bid_id=pk)
        return success_response(
            message="Bid deleted successfully.",
            status=status.HTTP_200_OK,
        )
