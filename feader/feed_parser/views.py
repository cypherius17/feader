from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import RSSItem, RSSSource
from .serializers import RSSItemSerializer, RSSSourceSerializer


class RSSItemListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'feed_parser/item_list.html'

    def get(self, request, format=None):
        queryset = RSSItem.objects.all().order_by("rss_source__id")
        serializer = RSSItemSerializer(queryset, many=True)
        return Response({'items': serializer.data})


class RSSItemDetailView(GenericViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'feed_parser/item_details.html'

    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = RSSItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect("/rss-items/")

    @action(methods=["get"], detail=True)
    def get(self, request, pk=None):
        rss_item = get_object_or_404(RSSItem, pk=pk) if pk else None
        serializer = RSSItemSerializer(rss_item) if rss_item else RSSItemSerializer()
        return Response({'serializer': serializer, 'rss_item': rss_item})

    @action(methods=["put"], detail=True)
    def put(self, request, pk):
        rss_item = get_object_or_404(RSSItem, pk=pk)
        serializer = RSSItemSerializer(rss_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect("/rss-items/")

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk):
        rss_item = get_object_or_404(RSSItem, pk=pk)
        rss_item.delete()
        return redirect("/rss-items/")
